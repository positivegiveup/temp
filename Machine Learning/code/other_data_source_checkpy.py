# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 13:17:15 2024

@author: pgn63
"""

import schedule
import time
import ccxt
import pandas as pd
from  trend_prediction_subfunction import data_preprocessing, First_LSTM_Prediction, Second_XGBoost_Prediction#預處理用
from  BTC_trading_strategy import auto_trading_strategy
from Buy_and_Sell_Point import buy_and_sell_point
from get_kline import get_and_store_klines, get_and_store_klines_v2,crypto_kline_data_from_other_source
from datetime import datetime, timedelta, timezone
symbol = 'BTC-USD' #改這邊換交易對
timeframe = '1d'
label_gap = 0.01
"""資料庫"""
data_path = 'test_check_kline_data.xlsx'
crypto_kline_data_from_other_source(symbol, timeframe, data_path)
