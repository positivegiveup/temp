# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 20:03:59 2023

@author: pgn63
"""

# trend_prediction_subfunction.py

import ccxt
import backtrader as bt
import datetime 
import time
import pandas as pd
from datetime import datetime, timedelta, timezone





#api帳密，交易對，k線資料庫，當日k線，活動紀錄資料庫
def auto_trading_strategy(api_key, secret, symbol, data_path, klines, record_book,label_gap, prediction_result):
    class CustomData(bt.Strategy):
        params = (
            ('datetime','Date'),
            ('open','Open'),
            ('high','High'),
            ('low','Low'),
            ('close','Close'),
            ('volume','Vol.'),
            ('label_gap',label_gap)

        )


        def __init__(self):

            self.order = None
            self.has_position = False
            self.buy_price = 0  # 紀錄已經買入的價格變量
            self.sell_flag = False
            self.bar_executed = 0
            self.cross = False
            self.trend_indicator = False
            self.price_updated = False
            

        def notify_order(self, order):
            if order.status in [order.Submitted, order.Accepted]:
                return
            if order.status in [order.Completed]:
                if order.isbuy():
                    self.log("Buy Executed at {:.2f}".format(order.executed.price))
                elif order.issell():
                    self.log("Sell Executed at {:.2f}".format(order.executed.price))
                self.bar_executed = len(self)
            elif order.status in [order.Canceled, order.Margin, order.Rejected]:
                self.log("Order Canceled/Margin/Rejected")
                self.counter = self.counter-1
            self.order = None

        def update_price(self):
           #API抓取最新價格
           ticker = exchange.fetch_ticker(self.symbol)
           self.last_price = ticker['last']
           self.price_updated = True

        def next(self):
            if btc_balance > 0:
                self.has_position = True
            elif btc_balance == 0:
                self.has_position = False
            else:
                print("Problem at account check")
            

            new_data = pd.DataFrame(klines, columns =['timestamp', 'open', 'high','low', 'close','volume'])
            new_data['timestamp'] = pd.to_datetime(new_data['timestamp'],unit = 'ms')
            new_data=new_data.iloc[-1] #可能會有問題?
            

            


            prediction_line=pd.read_excel(prediction_result)#呼叫資料
            prediction_line.set_index('timestamp',inplaxe = True)
            actual_col = prediction_line.columns[0]
            prediction_col = prediction_line.columns[0]
            buy_the_coin = False #用者兩個指標直接決定是否買進或賣出
            sell_the_coin = False 
            

            """交易邏輯"""
            if self.order:
                return           
            
            
            
            if ((self.close[0]-self.close[-1])/self.close[-1]) < 0.1:
                buy_the_coin = False 
                sell_the_coin = True #賣出
                self.sell_flag = True
            
            elif (prediction_line[actual_col][0] >= label_gap ):#升
                if prediction_line[prediction_col][0] >= label_gap :#升
                    buy_the_coin = True 
                    sell_the_coin = False #買進
                elif (prediction_line[prediction_col][0] <= (-label_gap) ):#降
                    buy_the_coin = False 
                    sell_the_coin = True #賣出
                    self.sell_flag = True
            elif(prediction_line[actual_col][0] < label_gap  and prediction_line[actual_col][0] >= (-label_gap)): #盤整
                if prediction_line[prediction_col][0] >= label_gap :#升
                    buy_the_coin = True 
                    sell_the_coin = False #買進
                else:
                    buy_the_coin = False 
                    sell_the_coin = True #賣出
                    self.sell_flag = True
            else:#降
               if prediction_line[prediction_col][0] >= label_gap :#升
                   buy_the_coin = True 
                   sell_the_coin = False #買進
               else:
                   buy_the_coin = False 
                   sell_the_coin = True #賣出
                   self.sell_flag = True

   

            """買入or賣出?""" 
            
            if not self.has_position:#確保倉位
                sell_the_coin = False

            """考慮到如果要下單的情況，獲取最新市場價格"""
            if not self.price_updated:
                self.update_price()
            #計算下單數量
            usdt_balance = exchange.fetch_balance()['total']['USDT']
            order_quantity = (usdt_balance*quantity_percentage)/self.last_price
            
            
            
            
            
            
            
            action_record = pd.DataFrame()#添加數據到全域變數 action_rercord
            """下買賣單"""
            
            if self.has_position and sell_the_coin:
                try:
                    market_sell_order = exchange.create_market_sell_order(symbol,order_quantity)
                    print("Market Sell Order Placed:",market_sell_order)
                    #賣出資訊儲存
                    action_record = action_record.append({
                        'timestamp':new_data['timestamp'].lioc[0],
                        'action':'sell',
                        'price':self.last_price,
                        'quantity':order_quantity,
                        'others':market_sell_order,
                        
                        })
                    action_record.to_excel(record_book,index=False)
                except ccxt.NetworkError as e:
                    print(f"Network error: {e}")
                except ccxt.ExchangeError as e:
                    print(f"Exahange error:{e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

            elif buy_the_coin:
                try:
                    market_buy_order = exchange.create_market_buy_order(symbol,order_quantity)
                    print("Market Buy Order Placed:",market_buy_order)
                    
                    action_record = action_record.append({
                        'timestamp':new_data['timestamp'].lioc[0],
                        'action':'buy',
                        'price':self.last_price,
                        'quantity':order_quantity,
                        'others':market_buy_order,
                        
                        })
                    action_record.to_excel(record_book,index=False)
                except ccxt.NetworkError as e:
                    print(f"Network error: {e}")
                except ccxt.ExchangeError as e:
                    print(f"Exahange error:{e}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    
                
            
            
            
            
            pass
        print("當日操作完成...")


    if __name__ == "__main__":
        print('Execute auto_trading program...')
        
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret,
        })
        balance = exchange.fetch_balance() #獲取帳戶餘額
        btc_balance = balance.get('total',{}).get('BTC',0) #BTC 餘額
        quantity_percentage = 0.2 #20% of USDT each order
        timeframe = '1d' #一天的數據
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe)
        
        """數據轉換成Pandas DataFrame"""
        ohlcv_df = pd.DataFrame(ohlcv,columns = ['timestamp','open','high','low','close','volume'])
        ohlcv_df['timestamp'] =pd.to_datetime(ohlcv_df['timestamp'],units = 'ms')
        ohlcv_df.set_index('timestamp',inplace = True)
        ohlcv_df.to_excel(data_path)

        cerebro = bt.Cerebro()
        cerebro.addstrategy(CustomData)

        ohlcv_df = pd.read_excel(data_path)
        data = bt.feeds.PandasData(dataname=ohlcv_df, datetime='Date', open='Open', high='High', low='Low', close='Close', volume='Vol.')

        cerebro.adddata(data)
        cerebro.run()

        print("起始投資組合價值: {:.2f}".format(cerebro.broker.getvalue()))


"""用法
# main_script.py

from trend_prediction_subfunction import backtest_strategy

if __name__ == "__main__":
    api_key = 'XKAvfGBvofQkU0dngtNgNBsWaszHQWTH8d5obA0dfUv01IXSqYP8vaJ0iC8wvoZI'
    secret = 'FOAyvIhI86n67wkWDz1cOFCyPFsvhQIFbnIrXLGjhLyiFtEj8wkF6pHd5kXBchO8'
    symbol = 'BTC/USDT'
    data_path = 'VM_online歷史數據.xlsx'

    auto_trading_strategy(api_key, secret, symbol, data_path, klines, record_book)
"""


















