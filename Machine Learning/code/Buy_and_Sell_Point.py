# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 13:34:14 2024

@author: pgn63
"""

import pandas as pd
import numpy as np
def buy_and_sell_point(data_path,output_path,gap):
    df = pd.read_excel(data_path)
    timestamp = df.columns[0]
    df.set_index(timestamp,inplace = True)
    df['Variation'] = (df['Close']-df['Close'].shift(1))/df['Close']
    #gap為0.01
    #1 表示買 -1表示賣 0不動
    df['Action'] = 0
    """
    if df['Predicted'] >= gap and df['Variation'] >= gap:
        if(df['Predicted'].shift(1) < gap or df['Actual_EMA'].shift(1) < gap):
            df.lioc['Action'] = 1 #買
    elif df['Actual_EMA']>=gap and df['Actual_EMA'].shift(1)<gap:
        df.lioc['Action'] = 1 #買
    elif df['Actual_EMA'] < gap and df['Actual_EMA'].shift(1) >=gap:
        df.lioc['Action'] = -1 #賣
    elif ((df['Predicted'] < gap and df['Actual_EMA'] < gap) and df['Predicted'].shift(1) >=gap):
        df.iloc['Action'] = -1 #賣
    """
    
    
    buy_condition = (df['Predicted'] >= gap) & (df['Variation'] >= gap) & ((df['Predicted'].shift(1) < gap) | (df['Actual_EMA'].shift(1) < gap))
    df.loc[buy_condition, 'Action'] = 1
    
    buy_condition = (df['Actual_EMA'] >= gap) & (df['Actual_EMA'].shift(1) < gap)
    df.loc[buy_condition, 'Action'] = 1
    
    sell_condition = (df['Actual_EMA'] < gap) & (df['Actual_EMA'].shift(1) >= gap)
    df.loc[sell_condition, 'Action'] = -1
    
    sell_condition = (df['Predicted'] < gap) & (df['Actual_EMA'] < gap) & (df['Predicted'].shift(1) >= gap)
    df.loc[sell_condition, 'Action'] = -1
    
    df.to_excel(output_path, index=True)
   
    


def buy_and_sell_point_v2(data_path,output_path,gap):
    df = pd.read_excel(data_path)
    timestamp = df.columns[0]
    df.set_index(timestamp,inplace = True)
    df['Variation'] = (df['Close']-df['Close'].shift(1))/df['Close']
    #gap為0.01
    #1 表示買 -1表示賣 0不動
    df['Action'] = 0
  
    buy_condition = (df['Predicted'] >= -gap) & (df['Variation'] >= gap) & ((df['Predicted'].shift(1) < -gap) | (df['Actual_EMA'].shift(1) < -gap))
    df.loc[buy_condition, 'Action'] = 1
    
    

    buy_condition = (df['Actual_EMA'] >= -gap) & (df['Actual_EMA'].shift(1) < -gap)
    df.loc[buy_condition, 'Action'] = 1
    
    
    
    sell_condition = (df['Actual_EMA'] < -gap) & (df['Actual_EMA'].shift(1) >= -gap)
    df.loc[sell_condition, 'Action'] = -1
    
    
    
    sell_condition = (df['Predicted'] < -gap) & (df['Actual_EMA'] < -gap) & (df['Predicted'].shift(1) >= -gap)
    df.loc[sell_condition, 'Action'] = -1
    
    
    
    df.to_excel(output_path, index=True)




def buy_and_sell_point_for_taiwan_stock_market(data_path,output_path,gap):
    df = pd.read_excel(data_path)
    timestamp = df.columns[0]
    df.set_index(timestamp,inplace = True)
    df['Variation'] = (df['Close']-df['Close'].shift(1))/df['Close']
    #gap為0.01
    #1 表示買 -1表示賣 0不動
    df['Action'] = 0
    
    if df['Predicted'] >= gap and df['Variation'] >= gap:
        if(df['Predicted'].shift(1) < gap or df['Actual_EMA'].shift(1) < gap):
            df.lioc['Action'] = 1 #買
    elif df['Actual_EMA']>=gap and df['Actual_EMA'].shift(1)<gap:
        df.lioc['Action'] = 1 #買
    elif df['Actual_EMA'] < gap and df['Actual_EMA'].shift(1) >=gap:
        df.lioc['Action'] = -1 #賣
    elif ((df['Predicted'] < gap and df['Actual_EMA'] < gap) and df['Predicted'].shift(1) >=gap):
        df.iloc['Action'] = -1 #賣
    """
    buy_condition = (df['Predicted'] >= gap) & (df['Variation'] >= gap) & ((df['Predicted'].shift(1) < gap) | (df['Actual_EMA'].shift(1) < gap))
    df.loc[buy_condition, 'Action'] = 1
    
    buy_condition = (df['Actual_EMA'] >= gap) & (df['Actual_EMA'].shift(1) < gap)
    df.loc[buy_condition, 'Action'] = 1
    
    sell_condition = (df['Actual_EMA'] < gap) & (df['Actual_EMA'].shift(1) >= gap)
    df.loc[sell_condition, 'Action'] = -1
    
    sell_condition = (df['Predicted'] < gap) & (df['Actual_EMA'] < gap) & (df['Predicted'].shift(1) >= gap)
    df.loc[sell_condition, 'Action'] = -1
    
    """
    #台股過於複雜的修正買賣訊號
    df['Action_Shift'] =df['Action'].shift(1)
    df['Modified_Action'] = 0
    
    buy_condition = (df['Action_Shift']+df['Action'] != 0 ) & (df['Action_Shift'] != df['Action'] ) & (df['Action_Shift'] == 1)
    df.loc[buy_condition, 'Modified_Action'] = 1
    
    sell_condition = (df['Action_Shift']+df['Action'] != 0) & (df['Action_Shift'] != df['Action'] ) & (df['Action_Shift'] == -1)
    df.loc[sell_condition, 'Modified_Action'] = -1
    
    df['Action'] = df['Modified_Action']
    df.drop(columns = ['Modified_Action','Action_Shift'],inplace = True)
    
   
    df.to_excel(output_path,index = True)
    
def buy_and_sell_point_for_taiwan_market_reference_index(data_path,output_path,gap):
    df = pd.read_excel(data_path)
    timestamp = df.columns[0]
    df.set_index(timestamp,inplace = True)
    df['Variation'] = (df['Close']-df['Close'].shift(1))/df['Close']
    df['Action'] = 0
    #variation, predicted,actual_EMA 三者取二 up 
    
    

    buy_condition = (
        ((df['Variation'] >= gap) & (df['Actual_EMA'] >= gap)) |
        ((df['Variation'] >= gap) & (df['Predicted'] >= gap))  |
        ((df['Actual_EMA'] >= gap) & (df['Predicted'] >= gap))
        )
    df.loc[buy_condition, 'Action'] = 2
    
    
    
    sell_condition = (
        ((df['Variation'] <= -gap) & (df['Actual_EMA'] <= -gap)) |
        ((df['Variation'] <= -gap) & (df['Predicted'] <= -gap))  |
        ((df['Actual_EMA'] <= -gap) & (df['Predicted'] <= -gap))
        )
    df.loc[sell_condition, 'Action'] = -2
    
    
    
    
    
    df.to_excel(output_path, index=True)


def cobination_version_crypto_strategy_and_trend_ref(data_path,output_path,gap):
    df = pd.read_excel(data_path)
    timestamp = df.columns[0]
    df.set_index(timestamp,inplace = True)
    df['Variation'] = (df['Close']-df['Close'].shift(1))/df['Close']
    #gap為0.01
    #1 表示買 -1表示賣 0不動
    df['Action'] = 0
    df['Index_1'] = 0 #之後可能會有更多指標，預先標1 以未來擴充做準備
    
    """趨勢指標_1"""
    upward_index = (
        ((df['Variation'] >= gap) & (df['Actual_EMA'] >= gap)) |
        ((df['Variation'] >= gap) & (df['Predicted'] >= gap))  |
        ((df['Actual_EMA'] >= gap) & (df['Predicted'] >= gap))
        )
    df.loc[upward_index, 'Index_1'] = 2
    
    downward_index = (
        ((df['Variation'] <= -gap) & (df['Actual_EMA'] <= -gap)) |
        ((df['Variation'] <= -gap) & (df['Predicted'] <= -gap))  |
        ((df['Actual_EMA'] <= -gap) & (df['Predicted'] <= -gap))
        )
    df.loc[downward_index, 'Index_1'] = -2


    """買賣建議"""
    buy_condition = (df['Predicted'] >= gap) & (df['Variation'] >= gap) & ((df['Predicted'].shift(1) < gap) | (df['Actual_EMA'].shift(1) < gap))
    df.loc[buy_condition, 'Action'] = 1
    
    buy_condition = (df['Actual_EMA'] >= gap) & (df['Actual_EMA'].shift(1) < gap)
    df.loc[buy_condition, 'Action'] = 1
    
    sell_condition = (df['Actual_EMA'] < gap) & (df['Actual_EMA'].shift(1) >= gap)
    df.loc[sell_condition, 'Action'] = -1
    
    sell_condition = (df['Predicted'] < gap) & (df['Actual_EMA'] < gap) & (df['Predicted'].shift(1) >= gap)
    df.loc[sell_condition, 'Action'] = -1
    
    df.to_excel(output_path, index=True)


