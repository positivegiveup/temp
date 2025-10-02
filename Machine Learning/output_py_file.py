# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 16:08:25 2024

@author: pgn63
"""

# -*- coding: utf-8 -*-

import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QSizePolicy, QLineEdit
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import Qt, QPointF
from PySide2 import QtCharts

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # ... 省略其他初始化設定 ...
        self.setGeometry(100, 100, 1500, 1440)
        self.setWindowTitle("Automatic Trading")

        # 设置背景
        
        background = QtWidgets.QLabel(self)
        background.setGeometry(0, 0, 1500, 1440)
        img = QtGui.QImage('背景.jpg')
        scaled_img = img.scaled(1500, 1440)
        background.setPixmap(QtGui.QPixmap.fromImage(scaled_img))
        
        # Logo
        logo = QtWidgets.QLabel(self)
        logo.setGeometry(5, 5, 90, 90)
        logo_img = QtGui.QImage("logo.jpg")
        scaled_logo = logo_img.scaled(90, 90)
        logo.setPixmap(QtGui.QPixmap.fromImage(scaled_logo))
        
        """表格1"""
        # 表格初始化部分...
        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(5, 120, 720, 360)
        self.table.setColumnCount(5)
        self.table.setRowCount(7)  # 調整行數為7，即顯示近7天的資料

        # 设置表头
        header_labels = ['timestamp','Open','High','Low','Close']
        self.table.setHorizontalHeaderLabels(header_labels)

        # 设置表格样式
        self.table.setStyleSheet('font-size:15px;color: black;font-weight:bold;background-color:#EAEAEA;border:2px solid #5B5B5B; border-radius:10px;text-align: center;')
        self.table.horizontalHeader().setStyleSheet('background-color: #78C7C7;color: black;font-weight:bold;border:2px solid #5B5B5B;border-radius:10px;')
        self.table.verticalHeader().setStyleSheet('background-color: #78C7C7;color: white;font-weight:bold;border:2px solid #5B5B5B;border-radius:10px;')

        # 初始数据加载到表格
        self.update_table()
        
        #更新表格按鈕
        self.update_button = QtWidgets.QPushButton('Update_Information',self)
        self.update_button.setGeometry(1310,500,150,30)
        self.update_button.setStyleSheet('font-size:15px;color: white ;font-weight:bold;background-color:black;border:2px solid #0000db; border-radius:10px;text-align: center;')
        self.update_button.clicked.connect(self.update_table)
        
        """表格2"""
        self.prediction_result = QtWidgets.QTableWidget(self)
        self.prediction_result.setGeometry(5,500,480,360)
        self.prediction_result.setColumnCount(5)
        self.prediction_result.setRowCount(7)  
        
        
        results = ['timestamp', 'Action','Buy_or_Sell']
        self.prediction_result.setHorizontalHeaderLabels(results)
        
        
        
        #加上推薦label
        self.recommendation_label = QtWidgets.QLabel('Recommendation_Operation',self)
        self.recommendation_label.setGeometry(750,600,300,30)
        self.recommendation_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)   
        self.recommendation_label.setStyleSheet('font-size:20px; color:pink; font-weight: bold; border: 2px solid #000000; padding: 5px;')

        
        self.update_result()
        
        
        
        """圖表1"""
        
        #圖表
        self.chart = QChart()
        self.chart.setTitle("Last-30-Day Chart")
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        
        self.open_series = QLineSeries()
        self.high_series = QLineSeries()
        self.low_series = QLineSeries()
        self.close_series = QLineSeries()
        
        
        self.chart.addSeries(self.open_series)
        self.chart.addSeries(self.high_series)
        self.chart.addSeries(self.low_series)
        self.chart.addSeries(self.close_series)
        
        
        
        self.chart.createDefaultAxes()
        self.chart_view = QChartView(self.chart)
        self.chart_view.setGeometry(740, 120, 720, 360)
        self.chart_view.setParent(self)
        self.update_chart()
        
        """下單表格"""
        self.order_table = QtWidgets.QTableWidget(self)
        self.order_table.setGeometry(500, 500, 240, 180)
        self.order_table.setColumnCount(0)
        self.order_table.setRowCount(3)  
        results = ['Trading_Pair','Price(USDT)','Buy/Sell']
        self.order_table.setVerticalHeaderLabels(results)
        
        
        self.param_name = QtWidgets.QLineEdit()
        self.param_price = QtWidgets.QLineEdit()
        self.order_table.insertColumn(0)
        self.order_table.setCellWidget(0,0,self.param_name)
        self.order_table.setCellWidget(1,0,self.param_price)
        #添加買賣按鈕
        self.buy_button = QtWidgets.QPushButton('BUY',self)
        self.sell_button = QtWidgets.QPushButton('SELL',self)
        self.buy_button.setGeometry(750, 500, 90,30)
        self.sell_button.setGeometry(850,500, 90,30)
        self.buy_button.setStyleSheet('font-size:15px;color: white;font-weight:bold;background-color:green;border:2px solid #0000db; border-radius:10px;text-align: center;')
        self.sell_button.setStyleSheet('font-size:15px;color: white;font-weight:bold;background-color:red;border:2px solid #0000db; border-radius:10px;text-align: center;')
        self.buy_button.clicked.connect(lambda:self.set_buy_sell('BUY'))
        self.sell_button.clicked.connect(lambda:self.set_buy_sell('SELL'))
        
        
        
        #添加下單按鈕
        self.place_order_button = QtWidgets.QPushButton('Sent_Order',self)
        self.place_order_button.setGeometry(750, 540, 190, 50)#換掉
        self.place_order_button.setStyleSheet('font-size:15px;color: white;font-weight:bold;background-color:black;border:2px solid #0000db; border-radius:10px;text-align: center;')
        self.place_order_button.clicked.connect(self.place_order)
        """#先不加
        #自動交易列表  self.order_table.setGeometry(500, 500, 240, 180)下面
        self.autotrading_table = QtWidgets.QTableWidget(self)
        self.autotrading_table.setGeometry(500,700,400,160)#暫時先設這樣
        self.autotrading_table.setColumnCount(3)
        self.autotrading_table.setRowCount(0)
        results= ['BTC_Balance','USDT_Balance','Discription']
        self.autotrading_table.setHorizontalHeaderLabels(results)
        
        #更新帳戶資料按鈕
        self.update_account_information = QtWidgets.QPushButton('Update_Account_Information',self)
        self.update_account_information.setGeometry(920,700,90,30)
        self.update_account_information.setStyleSheet('font-size:15px;color: white;font-weight:bold;background-color:black;border:2px solid #0000db; border-radius:10px;text-align: center;')
        self.update_account_information.clicked.connect(self.update_account)
        """
    def update_table(self):
        # 將您原有的更新表格的邏輯移植過來
        # 這裡假設您有一個名為 df 的 DataFrame 變數，包含要顯示的資料
        df = pd.read_excel('prediction_result.xlsx')

        # 我們只取近7天的資料
        last_7_days = df.tail(7)

        # 更新表格
        for row in range(7):
            for col, header in enumerate(['timestamp','Open','High','Low','Close']):
                item = QtWidgets.QTableWidgetItem(str(last_7_days.at[last_7_days.index[row], header]))
                self.table.setItem(row, col, item)
    
    
    def update_result(self):
        re = pd.read_excel('prediction_result.xlsx')
        last_7_days = re.tail(7)
        
        # 添加一列用于显示结果
        self.prediction_result.setColumnCount(3)  # 假设原表格有4列
        self.prediction_result.setHorizontalHeaderLabels(['timestamp', 'Action','Buy_or_Sell'])
        self.prediction_result.setRowCount(7)
        
        for row in range(7):
            timestamp = last_7_days.at[last_7_days.index[row], 'timestamp']
            action_label = last_7_days.at[last_7_days.index[row], 'Action']
            #Action = last_7_days.at[last_7_days.index[row], 'Buy_or_Sell']
            
            

            # 根据差值显示结果
            if action_label == 1:
                Action = 'BUY'
            elif 0.01 > action_label == 0:
                Action = 'HOLD'
            else:
                Action= 'SELL'

            # 更新表格
            item_timestamp = QtWidgets.QTableWidgetItem(str(timestamp))
            item_action_label = QtWidgets.QTableWidgetItem(str(action_label))
            item_action = QtWidgets.QTableWidgetItem(str(Action))

            
            self.prediction_result.setItem(row, 0, item_timestamp)
            self.prediction_result.setItem(row, 1, item_action_label)
            self.prediction_result.setItem(row, 2, item_action)
        # 更新推荐信息
        last_row_buy_sell = self.prediction_result.item(6, 2).text()
        if last_row_buy_sell == 'BUY':
            recommendation = 'Recommend Operation：BUY'
        elif last_row_buy_sell == 'SELL':
            recommendation = 'Recommend Operation：SELL'
        else:
            recommendation = 'Recommend Operation：HOLD'

        self.recommendation_label.setText(recommendation)
    
    
    def update_chart(self):
        df = pd.read_excel('prediction_result.xlsx')
        last_30_days = df.tail(30)
        last_30_days = last_30_days.sort_values(by='timestamp')
        
        self.open_series.clear()
        self.high_series.clear()
        self.low_series.clear()
        self.close_series.clear()
        
        
        for row in range(30):
            timestamp = last_30_days.at[last_30_days.index[row], 'timestamp'].timestamp()
            open_price = last_30_days.at[last_30_days.index[row], 'Open']
            high_price = last_30_days.at[last_30_days.index[row], 'High']
            low_price = last_30_days.at[last_30_days.index[row], 'Low']
            close_price = last_30_days.at[last_30_days.index[row], 'Close']
            
            
            # 在四個線段中分別添加資料點
            self.open_series.append(QPointF(float(timestamp), open_price))
            self.high_series.append(QPointF(float(timestamp), high_price))
            self.low_series.append(QPointF(float(timestamp), low_price))
            self.close_series.append(QPointF(float(timestamp), close_price))
            
            
        # 在此處更新圖表
        
        
        
        self.chart_view.chart().removeSeries(self.open_series)
        self.chart_view.chart().removeSeries(self.high_series)
        self.chart_view.chart().removeSeries(self.low_series)
        self.chart_view.chart().removeSeries(self.close_series)
        
        self.chart_view.chart().addSeries(self.open_series)
        self.chart_view.chart().addSeries(self.high_series)
        self.chart_view.chart().addSeries(self.low_series)
        self.chart_view.chart().addSeries(self.close_series)

        self.chart_view.chart().createDefaultAxes()
        self.chart_view.chart().setTitle("Last-30-Day Chart")
    
    def place_order(self):
        trading_pair = self.param_name.text()
        price = self.param_price.text()
        print(f'下單成功: {trading_pair}, 價格: {price}')
        self.place_order_button.setText('Order_Sented')
    def set_buy_sell(self,action):
        self.order_table.item(2, 0).setText(action)
    
    
    
    
if __name__ == "__main__":
    data_path = 'prediction_result.xlsx' #prediction_result_v2_check
    data = pd.read_excel(data_path)

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    app.quit()



