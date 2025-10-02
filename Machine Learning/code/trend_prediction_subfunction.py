# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 14:16:04 2023

@author: pgn63
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from tensorflow.keras.models import load_model
from xgboost import XGBRegressor

def data_preprocessing(input_data_path, output_data_path):
    df = pd.read_excel(input_data_path)
    timestamp = df.columns[0]
    df.set_index(timestamp,inplace = True)
    
    #preprocessing

    df['quote_score'] = (df['close'] - df['close'].shift(1)) / df['close'].shift(1)


    df['EMA'] = ((1/28)*df['quote_score'].shift(6)+
                 (2/28)*df['quote_score'].shift(5)+
                 (3/28)*df['quote_score'].shift(4)+
                 (4/28)*df['quote_score'].shift(3)+
                 (5/28)*df['quote_score'].shift(2)+
                 (6/28)*df['quote_score'].shift(1)+
                 (7/28)*df['quote_score'])




#製作RSI指標
    rsi_window_size=14#移動平均窗口大小
    df["Price_Change"]=df["close"].diff()#算每日價格變化
#上漲和下跌的平均值
    df["Gain"]=df["Price_Change"].apply(lambda x:x if x> 0 else 0)
    df["Loss"]=df["Price_Change"].apply(lambda x:x if x<0 else 0 )
    df["AVG_Gain"]=df["Gain"].rolling(window=rsi_window_size).mean()
    df["AVG_Loss"]=df["Loss"].rolling(window=rsi_window_size).mean()






#生成RSI
    df["RS"]=df["AVG_Gain"]/df["AVG_Loss"]
    df["RS"] = df["RS"].replace(-1, 0)

    df["RSI"]=100-(100/(1+df["RS"]))
    df=df.drop(["Price_Change","Gain","Loss","AVG_Gain","AVG_Loss","RS"],axis=1)

#製作MACD指標
    macd_short_window=12
    macd_long_window=26
    macd_signal_window=9
#短期EMA和長期EMA
    df["Short_EMA"]=df["close"].ewm(span=macd_short_window,adjust=False).mean()
    df["Long_EMA"]=df["close"].ewm(span=macd_long_window,adjust=False).mean()
#DIF值
    df["DIF"]=df["Short_EMA"]-df["Long_EMA"]
#計算MACD
    df["Signal_line"]=df["DIF"].ewm(span=macd_signal_window,adjust=False).mean()
#生成MACD
    df["MACD"]=df["DIF"]-df["Signal_line"]
    df=df.drop(["DIF","Signal_line",'Long_EMA','Short_EMA'],axis=1)

#計算CCI指標
    cci_window_size=20
    df["Typical_Price"]=(df["high"]+df["low"]+df["close"])/3
#計算典型價格的SMA
    df["SMA"]=df["Typical_Price"].rolling(window=cci_window_size).mean()
#計算平均差距
    mean_deviation=df["Typical_Price"].rolling(window=cci_window_size).mean()

#生成CCI
    df["CCI"]=(df["Typical_Price"]-df["SMA"])/(0.015*mean_deviation)
    df=df.drop(["Typical_Price","SMA",'high','low'],axis=1)


    df.to_excel(output_data_path,index = True)



def First_LSTM_Prediction(preprocessing_data,output_data,LSTM_Model_1,LSTM_Model_2):

    df = pd.DataFrame()
    df = pd.read_excel(preprocessing_data)
    df.set_index('timestamp',inplace = True)
    scaler = MinMaxScaler()
    columns_to_normalize = df.columns
    df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize]) 
    window_size = 7 #時間窗口7

    #匯入模型
    LSTM_model_1 = load_model(LSTM_Model_1)#'hybrid_LSTM_trend_prediction.h5'
    LSTM_model_2 = load_model(LSTM_Model_2)#hybrid_LSTM_trend_prediction2.h5

    #轉資料形狀
    x_test=[]
    for j in range(window_size,len(df)):
        x_test.append(df.iloc[j-window_size:j,0])
        
    x_test=np.array(x_test)
    x_test  = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    x_test = pd.DataFrame(x_test.reshape(x_test.shape[0], x_test.shape[1]), index=df.index[window_size:])
    #預測
    result_1 = LSTM_model_1.predict(x_test)
    result_2 = LSTM_model_2.predict(x_test)


    #形狀整理
    result_1 = np.squeeze(result_1)#2334
    result_2 = np.squeeze(result_2)
    df = df.iloc[window_size:]
    first_step_prediction_result = pd.DataFrame({
        'Predicted_EMA':result_1,
        'Predicted_Close':result_2
        
        },index = df.index)
    first_step_prediction_result.index = df['EMA'].index
    first_step_prediction_result.to_excel(output_data,index = True)

    
    
def Second_XGBoost_Prediction(data_path, preprocessing_data, first_step_result, prediction_result,xgb_model_weight):
    

    features = pd.read_excel(preprocessing_data)
    original_kline = pd.read_excel(data_path)
    first_results =  pd.read_excel(first_step_result)


#合併
    features.set_index('timestamp',inplace = True)
    first_results.set_index('timestamp',inplace = True)
    original_kline.set_index('timestamp',inplace = True)
    preprocessing_data = pd.concat([features, first_results], axis=1)
    preprocessing_data.drop(['open','volume','quote_score'],axis = 1,inplace = True)


#測試列
    target = pd.DataFrame()
    target['Final_EMA_Prediction'] = preprocessing_data['EMA'].shift(-1)
    num_features = len(preprocessing_data.columns)
    print(preprocessing_data)
    #架設model
    scaler = StandardScaler()
    preprocessing_data = scaler.fit_transform(preprocessing_data)
    xgboost_model = XGBRegressor(n_estimators=100, max_depth=3, learning_rate=0.1, num_features=num_features)
    loaded_model = XGBRegressor()
    loaded_model.load_model(xgb_model_weight)
    predictions = loaded_model.predict(preprocessing_data)
    print(predictions)
    print('Prediction Finished')
    predictions_result = pd.DataFrame({'Open': original_kline[original_kline.columns[0]],
                                       'High': original_kline[original_kline.columns[1]],
                                       'Low': original_kline[original_kline.columns[2]],
                                       'Close': original_kline[original_kline.columns[3]],
                                       'Actual_EMA': target['Final_EMA_Prediction'], 
                                       'Predicted': predictions})
    
    
    predictions_result.to_excel(prediction_result, sheet_name="predction_result", index=True)

   