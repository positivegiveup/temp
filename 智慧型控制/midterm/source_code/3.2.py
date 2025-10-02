import numpy as np
import math
import time

def clipped_poisson(lam, max_k):
    """
    Return poisson PMF clipped at max_k with remaining tail probability
    placed at max_k.
    """
    pmf = np.zeros(max_k + 1)
    for k in range(max_k):
        pmf[k] = math.exp(-lam) * lam**k / math.factorial(k)
    pmf[max_k] = 1 - np.sum(pmf)
    
    return pmf  

def build_rent_return_pmf(lambda_request, lambda_return, max_cars):
    """
    Return p(new_rentals, returns | initial_cars) as numpy array:
        p[initial_cars, new_rentals, returns]
    """
    pmf = np.zeros((max_cars+1, max_cars+1, max_cars+1))
    
    for init_cars in range(max_cars + 1):
        new_rentals_pmf = clipped_poisson(lambda_request, init_cars)
        for new_rentals in range(init_cars + 1):
            max_returns = max_cars - init_cars + new_rentals
            returns_pmf = clipped_poisson(lambda_return, max_returns)
            for returns in range(max_returns + 1):
                p = returns_pmf[returns] * new_rentals_pmf[new_rentals]
                pmf[init_cars, new_rentals, returns] = p
                
    return pmf

class JacksWorld(object):
    """Environment model of Jack's Car Rental"""
    def __init__(self, lambda_return1, lambda_return2,
                 lambda_request1, lambda_request2, max_cars):
        # pre-build the rentals/returns pmf for each location
        self.rent_return_pmf = []
        self.rent_return_pmf.append(build_rent_return_pmf(lambda_request1,
                                                      lambda_return1,
                                                      max_cars))
        self.rent_return_pmf.append(build_rent_return_pmf(lambda_request2,
                                                      lambda_return2,
                                                      max_cars))
        self.max_cars = max_cars
        
    def get_transition_model(self, s, a):
        """
        Return 2-tuple:
            1. p(s'| s, a) as dictionary:
                keys = s'
                values = p(s' | s, a)
            2. E(r | s, a, s') as dictionary:
                keys = s'
                values = E(r | s, a, s')
        """
        # 調整汽車轉移：員工免費轉移 1 輛車從地點 1 到地點 2
        effective_a = a  # 實際需要計算費用的轉移數量
        if a >= 1:
            # 如果從地點 1 轉移到地點 2 的數量 >= 1，則 1 輛車免費
            move_cost = -(a - 1) * 2 if a > 1 else 0  # 免費轉移 1 輛，其餘每輛 2 美元
        else:
            # 從地點 2 到地點 1 的轉移仍需支付每輛 2 美元
            move_cost = -math.fabs(a) * 2

        # 執行汽車轉移
        s = (s[0] - a, s[1] + a)  # 移動 a 輛車從地點 1 到地點 2

        # 計算停車費用：如果過夜汽車數量超過 10 輛，則每個地點額外支付 4 美元
        parking_cost = 0
        for loc_cars in s:
            if loc_cars > 10:
                parking_cost -= 4  # 每個地點超過 10 輛支付 4 美元

        # 計算總移動和停車費用
        move_reward = move_cost + parking_cost

        t_prob, expected_r = ([{}, {}], [{}, {}])
        for loc in range(2):
            morning_cars = s[loc]
            rent_return_pmf = self.rent_return_pmf[loc]
            for rents in range(morning_cars + 1):
                max_returns = self.max_cars - morning_cars + rents
                for returns in range(max_returns + 1):
                    p = rent_return_pmf[morning_cars, rents, returns]
                    if p < 1e-5:
                        continue
                    s_prime = morning_cars - rents + returns
                    r = rents * 10  # 每輛車租賃收入 10 美元
                    t_prob[loc][s_prime] = t_prob[loc].get(s_prime, 0) + p
                    expected_r[loc][s_prime] = expected_r[loc].get(s_prime, 0) + p * r
        
        # 合併兩個地點的概率和期望回報
        t_model, r_model = ({}, {})
        for s_prime1 in t_prob[0]:
            for s_prime2 in t_prob[1]:
                p1 = t_prob[0][s_prime1]  # 地點 1 的 p(s' | s, a)
                p2 = t_prob[1][s_prime2]  # 地點 2 的 p(s' | s, a)
                t_model[(s_prime1, s_prime2)] = p1 * p2
                # 計算期望回報，需標準化
                norm_E1 = expected_r[0][s_prime1] / p1
                norm_E2 = expected_r[1][s_prime2] / p2
                r_model[(s_prime1, s_prime2)] = norm_E1 + norm_E2 + move_reward
                
        return t_model, r_model
    
# 初始化環境（修正前述問題中的參數）
max_cars = 20
jacks = JacksWorld(lambda_return1=4, lambda_return2=2,  # 修正地點 1 的平均歸還為 4
                 lambda_request1=3, lambda_request2=4, max_cars=max_cars)

# 初始化價值函數
V = np.zeros((max_cars+1, max_cars+1))
states = [(s0, s1) for s0 in range(max_cars+1) for s1 in range(max_cars+1)]
gamma = 0.85  # 修正折扣率為 0.85

start_time = time.time()
# 價值迭代
theta = 0.5  # V(s) 停止閾值
print('Worst |V_old(s) - V(s)| delta:')
for k in range(100):
    delta = 0
    V_old = V.copy()
    V = np.zeros((max_cars+1, max_cars+1))
    for s in states:
        v_best = -1000
        max_a = min(5, s[0], max_cars-s[1])
        min_a = max(-5, -s[1], -(max_cars-s[0]))
        for a in range(min_a, max_a+1):
            t_model, r_model = jacks.get_transition_model(s, a)            
            v_new = 0
            for s_prime in t_model:
                p = t_model[s_prime]
                r = r_model[s_prime]
                v_new += p * (gamma * V_old[s_prime] + r)
            v_best = max(v_best, v_new)
        V[s] = v_best
        delta = max(delta, abs(V[s] - V_old[s]))
    print('Iteration {}: max delta = {:.2f}'.format(k, delta))
    if delta < theta: break

# 從 V(s) 中提取策略
pi = np.zeros((max_cars+1, max_cars+1), dtype=np.int16)
for s in states:
    best_v = -1000
    max_a = min(5, s[0], max_cars-s[1])
    min_a = max(-5, -s[1], -(max_cars-s[0]))
    for a in range(min_a, max_a+1):
        t_model, r_model = jacks.get_transition_model(s, a)
        v = 0
        for s_prime in t_model:
            p = t_model[s_prime]
            r = r_model[s_prime]
            v += p * (gamma * V[s_prime] + r)
        if v > best_v:
            pi[s] = a
            best_v = v
            
print('\nValue iteration done, final policy:')            
print(pi)
            
print("\n--- {:.2f} seconds ---".format(time.time() - start_time))