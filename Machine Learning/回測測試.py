# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 22:46:50 2024

@author: pgn63
"""
import datetime
import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt
class strategy(bt.Strategy):
    params = (
        ('gap',0.01),
        )
    def __init__(self):
        print("Start Date:", self.data.datetime.date(ago=0).strftime("%Y-%m-%d"))
        print("End Date:", self.data.datetime.date(ago=-1).strftime("%Y-%m-%d"))
        self.label = self.datas[0].volume #直接用open代替
        self.close = self.datas[0].close
        self.gap = self.params.gap
        self.has_position = False
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log("Buy Executed at {:.2f}".format(order.executed.price))
            elif order.issell():
                self.log("Sell Executed at {:.2f}".format(order.executed.price))
            self.bar_executed = self.data.datetime.date(ago=0)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log("Order Canceled/Margin/Rejected")
        self.order = None
    
    def next(self):
        
        #交易比例
        trade_pct =0.1
        """
        1.存股策略改0.1或其他數字  
        2.波段策略改1
        """
        trade_size=int(self.broker.getvalue()*trade_pct/self.close[0])
        
        


        
        if self.label == 1:

            self.buy(size = trade_size)
            #self.log("Buy Create {:.2f}".format(self.close[0]))
            self.has_position = True

        
        if self.has_position:
            if self.label == -1:

                self.sell(size = trade_size)
                #self.log("Sell Create {:.2f}".format(self.close[0]))
                self.has_position = False
        
        
        self.log("Capital {:.2f}".format(self.broker.getvalue()))

       
       
       

    def log(self,txt,dt = None):
        dt = self.datas[0].datetime.date(ago=0)
        log_data.loc[len(log_data)] = [dt, txt]
        print("{} {}".format(dt.isoformat(), txt))
        

    
if __name__ == '__main__':

    cerebro  = bt.Cerebro()
    
    #虛擬初始資金
    cerebro.broker.set_cash(1000000000000)
    cerebro.broker.setcommission(commission=0.001)
    
    
    
    #導入資料
    prediction_data = 'prediction_result.xlsx'
    
    #設定回測範圍
    year = 2024
    
    data = bt.feeds.PandasData(
        dataname=pd.read_excel(prediction_data),
        
        fromdate=datetime.datetime(year, 1,1),
        todate=datetime.datetime(year, 12,31),
        datetime="timestamp",
        open="Open",
        high="High",
        low="Low",
        close="Close",
        volume ='Action',
        openinterest=None,

    )
    
    
    
    ##添加歷史數據到回測系統
    cerebro.adddata(data)
    
    #添加策略到回測系統
    cerebro.addstrategy(strategy)
    #紀錄
    log_data = pd.DataFrame(columns=['Date', 'Log Message'])
    #初始資金
    initial_capital = float(format(cerebro.broker.getvalue()))
    #進行回測
    result = cerebro.run()
    # 檢查回測是否成功完成
    if result:
        print('Ending Portfolio Value: %.2f' % cerebro.broker.getvalue())
    else:
        print('Backtest did not finish successfully.')
    #結果
    final_capital = float(format(cerebro.broker.getvalue()))
    profit_and_loss = (final_capital - initial_capital)
    capital_growth_rate = (profit_and_loss / initial_capital) * 100
    
    #報酬率
    print("Capital Growth Rate: {:.2f}%".format(capital_growth_rate))
    
    

    data_df = pd.read_excel(prediction_data)
    data_df['timestamp'] = pd.to_datetime(data_df['timestamp'])
    log_data['Date'] = pd.to_datetime(log_data['Date'])

    plt.figure(figsize=(14, 7))
    plt.plot(data_df['timestamp'], data_df['Close'], label='Close Price')

    # Extract buy points
    buy_points = log_data[log_data['Log Message'].str.contains('Buy Executed')]
    buy_prices = buy_points['Log Message'].str.extract(r'(\d+\.\d+)').astype(float)
    buy_points = buy_points.assign(Close=buy_prices)

    # Extract sell points
    sell_points = log_data[log_data['Log Message'].str.contains('Sell Executed')]
    sell_prices = sell_points['Log Message'].str.extract(r'(\d+\.\d+)').astype(float)
    sell_points = sell_points.assign(Close=sell_prices)

    plt.scatter(buy_points['Date'], buy_points['Close'], color='red', marker='^', label='Buy')
    plt.scatter(sell_points['Date'], sell_points['Close'], color='green', marker='v', label='Sell')

    plt.plot(data_df['timestamp'], data_df['Index_2'], label='120 Day SMA', linestyle='--')    

    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Backtest Results with Buy/Sell Points')
    plt.legend()
    plt.show()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    