# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:52:22 2024

@author: pgn63
"""
import schedule
import time
import ccxt
import pandas as pd
from  trend_prediction_subfunction import data_preprocessing, First_LSTM_Prediction, Second_XGBoost_Prediction#預處理用
from  BTC_trading_strategy import auto_trading_strategy
from Buy_and_Sell_Point import buy_and_sell_point,buy_and_sell_point_for_taiwan_market_reference_index, cobination_version_crypto_strategy_and_trend_ref
from get_kline import get_and_store_klines,crypto_kline_data_from_other_source
from datetime import datetime, timedelta, timezone
def run_daily_routine(symbol, timeframe, data_path, check_symbol,prediction_result, check_prediction_result):
    print('Running daily routine at {}'.format(datetime.now()))
    
    """密鑰&交易資訊"""
    api_key = 'tI5stusyJOWv5EQsWeko2PspaJ0KseBVFmSlXimMlkiIiDOyOfj2zpEaPKygrVC6'
    secret = 'IWrubycoG3mYssDswLjcqMPW2O5eckDGby6d85g93dBrH7VxwmkBVq4SUZJHXmM8'
    label_gap = 0.007 #(buy)
    #label_sell_gap = 0.01
    
    
    
    """資料庫"""
    preprocessing_data = 'preprocessing_data.xlsx' #前處理的暫存
    first_step_result = 'first_step_result.xlsx'#第一步預測的暫存
    #record_book = 'VM_活動紀錄表_.xlsx'
    """交易資料檢查所需檔案"""
    check_data_storage = 'test_check_kline_data.xlsx' #專屬BTC
    check_prediction_result = 'prediction_result_v2_check.xlsx'
    
    
    """預測model"""
    LSTM_Model_1 = 'hybrid_LSTM_trend_prediction.h5'
    LSTM_Model_2 = 'hybrid_LSTM_trend_prediction2.h5'
    XGBoost = 'hybrid_xgboost_model_weights.h5'
    
    
    
    """進行AI運算"""
    #獲取Kline
    print(symbol)
    klines = get_and_store_klines(api_key, secret, symbol, timeframe, data_path)
    #klines= get_and_store_klines_v2(symbol, timeframe, data_path)
    
    
    
    #資料前處理
    data_preprocessing(data_path, preprocessing_data) #output_data_path 為預處理的資料(放在excel)
    
    #預測第一步
    First_LSTM_Prediction(preprocessing_data,first_step_result,LSTM_Model_1,LSTM_Model_2)#output_data為預測值，要丟到第2層
    
    #預測第二步
    Second_XGBoost_Prediction(data_path, preprocessing_data, first_step_result, prediction_result,XGBoost)
    
    #生成交易指標
    #buy_and_sell_point(prediction_result,prediction_result,label_gap)

    
    #升級版
    cobination_version_crypto_strategy_and_trend_ref(prediction_result,prediction_result,label_gap)
    
    
    #開始交易
    #auto_trading_strategy(api_key, secret, symbol, data_path, klines, record_book,label_gap, prediction_result)
    
    
    
    """Dobule_Check_Procedure"""
    """

    crypto_kline_data_from_other_source(check_symbol, timeframe, check_data_storage)
    
    #資料前處理
    data_preprocessing(data_path, preprocessing_data) #output_data_path 為預處理的資料(放在excel)
    
    #預測第一步
    First_LSTM_Prediction(preprocessing_data,first_step_result,LSTM_Model_1,LSTM_Model_2)#output_data為預測值，要丟到第2層
    
    #預測第二步
    Second_XGBoost_Prediction(data_path, preprocessing_data, first_step_result, check_prediction_result,XGBoost)
    
    #生成交易指標
    #buy_and_sell_point(check_prediction_result,check_prediction_result,label_gap)
    cobination_version_crypto_strategy_and_trend_ref(check_prediction_result,check_prediction_result,label_gap)
    """