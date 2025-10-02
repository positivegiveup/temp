from collections import defaultdict
from pprint import pprint
import numpy as np
import tqdm
import logging
import pickle

logging.basicConfig(level=logging.INFO)

DISCRETIZATION_POSITION, DISCRETIZATION_VELOCITY = 15, 15
NUM_ITERATIONS = 200
NUMBER_OF_SAMPLES = 50

def discretize_position(position, n):
    space = np.linspace(-1.2, 0.6, n)
    position = np.clip(position, -1.2, 0.6)
    for i in range(n):
        if position < space[i]:
            return i - 1
    return n - 1

def discretize_velocity(velocity, n):
    space = np.linspace(-0.07, 0.07, n)
    velocity = np.clip(velocity, -0.07, 0.07)
    for i in range(n):
        if velocity < space[i]:
            return i - 1
    return n - 1

def discretize(position, velocity, discretization):
    return discretize_position(position, discretization[0]), discretize_velocity(velocity, discretization[1])


def sample_position_from_discretized(position, n):
    space = np.linspace(-1.2, 0.6, n)
    if position==n-1:
        return np.random.uniform(space[position], space[position]+0.1)

    return np.random.uniform(space[position], space[position+1])

def sample_velocity_from_discretized(velocity, n):
    space = np.linspace(-0.07, 0.07, n)
    if velocity==n-1:
        return np.random.uniform(space[velocity], space[velocity]+0.01)
    return np.random.uniform(space[velocity], space[velocity+1])

def map_states_to_continuous(states, discretization):
    return [(
                sample_position_from_discretized(state[0], discretization[0]), 
                sample_velocity_from_discretized(state[1], discretization[1])
            ) 
            # in state for states
            for state in states]


def compute_new_velocity(position, velocity, action):
    new_velocity = velocity + 0.001 * (action-1) - 0.0025 * np.cos(3 * position)
    return np.clip(new_velocity, -0.07, 0.07)

def compute_new_position(position, velocity):
    new_position = position + velocity
    return np.clip(new_position, -1.2, 0.6)


class MDP:
    def __init__(self, discretization=(DISCRETIZATION_POSITION, DISCRETIZATION_VELOCITY)):
        """
        在MDP中, 5 tuple (S, A, P, R, γ):
        - S: 狀態空間(離散化的位置和速度)。
        - A: 動作空間(0: 減速、1: 無動作、2: 加速)。
        - P: 轉移概率 P(s'|s,a), func.計算。
        - R: 獎勵函數 R(s,s'), func.計算。
        - γ: 折扣因子,平衡即時與未來獎勵。

        參數: 
            discretization: 狀態空間, 所有離散化的 (位置, 速度)。
        """
        # discount factor for future rewards, typically close to 1, 
        # to prioritize long-term rewards.
        self.gamma = 0.99
        
        # Discretization levels for position and velocity, defining the state space.
        self.discretization = discretization
        self.discretization_position = discretization[0]
        self.discretization_velocity = discretization[1]

        self.states = {(i, j) for i in range(self.discretization_position) for j in range(self.discretization_velocity)}

        # In MDP, actions A(s) are available choices at each state
        self.actions = [0, 1, 2]
        
        # Compute P(s' | s, a), the probability of transitioning to state s' given state s and action a.
        print("Computing transition probabilities")
        self.transition_probabilities = self.compute_transition_probabilities()
        print("Transition probabilities computed")
        
        print("Computing rewards")
        # Compute R(s, s'), the reward for transitioning from s to s'.
        self.rewards = self.compute_rewards()
        print("Rewards computed")

    def compute_transition_probabilities(self):
        """
        計算MDP的轉移概率 P(s'|s,a)。

        在MDP中,表示從狀態 s 採取動作 a 後到達狀態 s' 的概率。
        Mountain Car的連續動態通過以下方式近似: 
        1. 在每個離散區間內採樣連續狀態。
        2. 應用狀態轉移模型
        3. 離散化結果狀態並累積概率。

        返回: 
            defaultdict: 映射 (state, action, new_state) 到概率值。
        """
        transition_probabilities = defaultdict(lambda: 0)
        for state in self.states:
            discrete_position, discrete_velocity = state
            for action in self.actions:
                for _ in range(NUMBER_OF_SAMPLES):
                    continuous_position = sample_position_from_discretized(discrete_position, self.discretization_position)
                    continuous_velocity = sample_velocity_from_discretized(discrete_velocity, self.discretization_velocity)

                    new_velocity = compute_new_velocity(continuous_position, continuous_velocity, action)
                    new_position = compute_new_position(continuous_position, new_velocity)

                    new_discrete_state = discretize(new_position, new_velocity, self.discretization)
                    
                    #transition_probabilities[(state, action, new_discrete_state)] -= 1 / NUMBER_OF_SAMPLES
                    transition_probabilities[(state, action, new_discrete_state)] += 1 / NUMBER_OF_SAMPLES
        return transition_probabilities
    
    
    def compute_rewards(self):
        """
        計算MDP的獎勵函數 R(s,s')。

        在MDP中,表示從 s 轉移到 s' 的即時獎勵。
        在Mountain Car問題中(課程05: 動態規劃): 
        - 默認獎勵為 -1,懲罰每一步以鼓勵快速到達目標。
        - 當轉移到目標狀態(位置 >= 0.5)時,獎勵為 0,表示成功。

        返回: 
            defaultdict: 映射 (state, new_state) 到獎勵值。
        """
        rewards = defaultdict(lambda: -1)

        for state in self.states:
            for action in self.actions:
                for new_state in self.states:
                    # Check if new_state corresponds to position >= 0.5.
                    # Convert discretized position to continuous to compare with goal.
                    position = sample_position_from_discretized(new_state[0], self.discretization_position)
                    if position >= 0.5:
                        rewards[(state, new_state)] = 0
        return rewards
    

# Now that we have defined the MDP of the mountain car problem, we can use Value Iteration to solve it

def value_iteration(mdp, num_iterations=NUM_ITERATIONS):
    """
    執行價值迭代,計算最佳價值函數 V*(s)。

    價值迭代(課程05: 動態規劃)通過迭代應用貝爾曼最優性方程估計 V*(s),
    表示從狀態 s 開始的最大期望累積獎勵: 
        V_{k+1}(s) = max_a Σ_{s'} P(s'|s,a) [ R(s,s') + γ V_k(s') ]
    當 k → ∞ 時,收斂至 V*(s),為最佳策略提供基礎。

    參數: 
        mdp: 包含狀態、動作、轉移、獎勵和 γ 的MDP對象。
        num_iterations: 迭代次數。

    返回: 
        dict: 映射狀態到最佳價值 V*(s)。
    """
    V = {state: 0 for state in mdp.states}
    for _ in tqdm.tqdm(range(num_iterations)):
        for state in mdp.states:
            V[state] = max(
                sum(mdp.transition_probabilities.get((state, action, new_state), 0) * 
                    (mdp.rewards.get((state, new_state), -1) + mdp.gamma * V[new_state]) 
                    # in new_state for mdp.states
                    for new_state in mdp.states)
                # in action for mdp.actions
                for action in mdp.actions
            )
    return V

def get_policy(mdp, V):
    """
    從價值函數 V*(s) 導出最佳策略 π*(s)。

    在MDP中,最佳策略 π*(s) 選擇最大化期望累積獎勵的動作(課程05): 
        π*(s) = argmax_a Σ_{s'} P(s'|s,a) [ R(s,s') + γ V*(s') ]
    給定 V*(s),此貪婪策略是最優的。

    參數: 
        mdp: 包含狀態、動作、轉移、獎勵和 γ 的MDP對象。
        V: 最佳價值函數,映射狀態到價值。

    返回: 
        dict: 映射狀態到最佳動作。
    """
    policy = {}
    for state in mdp.states:
        policy[state] = max(mdp.actions, key=lambda action: 
            sum(mdp.transition_probabilities.get((state, action, new_state), 0) * 
                (mdp.rewards.get((state, new_state), -1) + mdp.gamma * V[new_state])
                # in new_state for mdp.states))
                for new_state in mdp.states))
    return policy


if __name__ == "__main__":
    logging.info("Computing MDP")
    mdp = MDP()
    logging.info("MDP computed")

    logging.info("Computing Value Iteration")
    V = value_iteration(mdp)
    logging.info("Value Iteration computed")

    logging.info("Computing policy")
    policy_mount_car = get_policy(mdp, V)
    logging.info("Policy computed")

    # save policy to file using pickle
    with open("policy_mountain_car_new_reward.pkl", "wb") as f:
        pickle.dump(policy_mount_car, f)
