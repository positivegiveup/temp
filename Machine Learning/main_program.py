# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 23:02:32 2023

@author: pgn63
"""

import schedule
import time
import ccxt
import pandas as pd
from  trend_prediction_subfunction import data_preprocessing, First_LSTM_Prediction, Second_XGBoost_Prediction#預處理用
from  BTC_trading_strategy import auto_trading_strategy
from Buy_and_Sell_Point import *
from get_kline import get_and_store_klines,crypto_kline_data_from_other_source, get_data_from_crypto_market,transform_US_stock_market_data_type
from datetime import datetime, timedelta, timezone

def run_daily_routine():
    print('Running daily routine at {}'.format(datetime.now()))
    
    """填資料"""
    coins="SOL"
    
    
    """密鑰&交易資訊"""
    api_key = '~~'
    secret = '~~'
    symbol = f'{coins}-USD' 
    timeframe = '1d'
    label_gap = 0.003 #(buy)
    weight_gap = 0.003
    #label_sell_gap = 0.01
    time_frame = 365
    
    
    """資料庫"""
    data_path = f'{coins}_historical_data.xlsx' #原始資料庫 #換不同的交易對記得要改   VM_online歷史數據 ALTCOIN歷史資料 Demo專用.xlsx(gap0.007)
    preprocessing_data = 'preprocessing_data.xlsx' #前處理的暫存
    first_step_result = 'first_step_result.xlsx'#第一步預測的暫存
    prediction_result = 'prediction_result.xlsx' #預測結果
    #record_book = 'VM_活動紀錄表_.xlsx'
    """交易資料檢查所需檔案"""
    check_symbol = 'BTC-USD' #換成coinbase交易所的資料
    check_data_storage = 'test_check_kline_data.xlsx' #專屬BTC
    check_prediction_result = 'prediction_result_v2_check.xlsx'
    
    
    """預測model"""
    LSTM_Model_1 = 'hybrid_LSTM_trend_prediction.h5'
    LSTM_Model_2 = 'hybrid_LSTM_trend_prediction2.h5'
    XGBoost = 'hybrid_xgboost_model_weights.h5'
    
    
    
    """進行AI運算"""
    #獲取Kline
    print(symbol)
    klines = get_data_from_crypto_market(symbol, data_path, time_frame)
    #klines= get_and_store_klines_v2(symbol, timeframe, data_path)
    transform_US_stock_market_data_type(data_path)
    
    
    #資料前處理
    data_preprocessing(data_path, preprocessing_data) #output_data_path 為預處理的資料(放在excel)
    
    #預測第一步
    First_LSTM_Prediction(preprocessing_data,first_step_result,LSTM_Model_1,LSTM_Model_2)#output_data為預測值，要丟到第2層
    
    #預測第二步
    Second_XGBoost_Prediction(data_path, preprocessing_data, first_step_result, prediction_result,XGBoost)
    


    
    #升級版
    cobination_version_crypto_strategy_and_trend_ref(prediction_result,prediction_result,label_gap)
    """盤勢不亂用"""

    
    
    
    
   
    


run_daily_routine()
