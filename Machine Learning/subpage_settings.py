# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:08:24 2024

@author: pgn63
"""

import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from crypto_prediction_sub import run_daily_routine
import ccxt
class sub_page1_information_table(QMainWindow):
    data_ready = pyqtSignal(dict)#定義要傳過去的資訊
    
    def __init__(self):
        super().__init__()
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 10000, 6000)
        background_pixmap = QPixmap('背景.jpg')
        self.background_label.setPixmap(background_pixmap)
        self.background_label.lower()
        self.background_label.setStyleSheet("background-image: url('背景.jpg'); background-size: cover;")
        
        
        # 设置窗口标题和大小
        self.setWindowTitle("Real Time Testing Settings")
        self.resize(400, 200)
        
        # 主 widget 和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # 标题标签
        self.title_label = QLabel("Trading Informations and Parameters Settings")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
        self.layout.addWidget(self.title_label)
        #說明標籤
        self.commentary_label = QLabel('Using Guide - Default Example')
        self.commentary_label.setAlignment(Qt.AlignCenter)
        self.commentary_label.setStyleSheet("color: white; font-weight: bold; font-size: 18px;font-weight: bold; font-size: 18px;")
        self.commentary_label.raise_()
        self.layout.addWidget(self.commentary_label)
        self.commentary_content = QLabel(
            'symbols = BTC/USDT '
            'timeframe = 1d '
            'data_path = VM_online歷史數據.xlsx\n '
            'check_symbol = BTC-USD '
            'prediction_result = prediction_result.xlsx '
            'check_prediction_result = prediction_result_v2_check.xlsx '
            )
        self.commentary_content.setAlignment(Qt.AlignCenter)
        self.commentary_content.setStyleSheet("color: white; font-weight: bold; font-size: 16px;font-weight: bold; font-size: 16px; border: 2px solid #D8BFD8;")
        self.layout.addWidget(self.commentary_content)
        self.commentary_content.raise_()
        self.table = QTableWidget(1, 6)
        self.table.setHorizontalHeaderLabels(["symbols", "time_frame", "data_path", "check_symbol",'prediction_result','check_prediction_result'])
        self.layout.addWidget(self.table)
        
        

        
        # 按钮布局
        self.button_layout = QHBoxLayout()
        
        # 按钮

        
        self.crypto_button = QPushButton("Crypto Mode")
        self.crypto_button.clicked.connect(self.crypto_function)
        self.button_layout.addWidget(self.crypto_button)
        
        self.tw_stock_button = QPushButton("TW Mode")
        self.tw_stock_button.clicked.connect(self.tw_stock_function)
        self.button_layout.addWidget(self.tw_stock_button)
        
        self.us_stock_button = QPushButton("US Mode")
        self.us_stock_button.clicked.connect(self.us_stock_function)
        self.button_layout.addWidget(self.us_stock_button)
        
        self.layout.addLayout(self.button_layout)
        

        
        
    def crypto_function(self):
        print("Crypto button clicked")
        
        
        symbols = []
        timeframe = []
        data_path = []
        check_symbol = []
        prediction_result = []
        check_prediction_result = []
        try:
            for row in range(self.table.rowCount()):
                symbols.append(self.table.item(row, 0).text())
                timeframe.append(self.table.item(row, 1).text())
                data_path.append(self.table.item(row, 2).text())
                check_symbol.append(self.table.item(row, 3).text())
                prediction_result.append(self.table.item(row, 4).text())
                check_prediction_result.append(self.table.item(row, 5).text())
        except Exception as e:
            print('No settings. Using default values.')
        
        
        try:
            symbols = ", ".join([self.table.item(row, 0).text() for row in range(self.table.rowCount())])
            timeframe = ", ".join([self.table.item(row, 1).text() for row in range(self.table.rowCount())])
            data_path = ", ".join([self.table.item(row, 2).text() for row in range(self.table.rowCount())])
            check_symbol = ", ".join([self.table.item(row, 3).text() for row in range(self.table.rowCount())])
            prediction_result = ", ".join([self.table.item(row, 4).text() for row in range(self.table.rowCount())])
            check_prediction_result = ", ".join([self.table.item(row, 5).text() for row in range(self.table.rowCount())])
        except Exception as e:
            print('No settings. Using default values.')
            symbols = 'BTC/USDT'
            timeframe = '1d'
            data_path = 'VM_online歷史數據.xlsx'
            check_symbol = 'BTC-USD'
            prediction_result = 'prediction_result.xlsx'
            check_prediction_result = 'prediction_result_v2_check.xlsx'
            
  
        
        run_daily_routine(symbols,
                          timeframe, 
                          data_path, 
                          check_symbol,
                          prediction_result,
                          check_prediction_result,
                          )
        
        self.page1 = SubPage1()
        self.setCentralWidget(self.page1)
        self.page1.show()
    def tw_stock_function(self):
        print("台股 button clicked")

        


    def us_stock_function(self):
        print("美股 button clicked")

    
    


class SubPage1(QMainWindow):
    def __init__(self):
        super().__init__()
        
        
        self.showing_days = 30

        
        self.setGeometry(100, 100, 1500, 1440)
        self.setWindowTitle("Automatic Trading")

        # Background image
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

        # Table 1
        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(5, 120, 720, 360)
        self.table.setColumnCount(5)
        self.table.setRowCount(self.showing_days)
        header_labels = ['timestamp', 'Open', 'High', 'Low', 'Close']
        self.table.setHorizontalHeaderLabels(header_labels)
        self.update_table()

        # Update table button
        self.update_button = QtWidgets.QPushButton('Update_Information', self)
        self.update_button.setGeometry(1310, 500, 150, 30)
        self.update_button.clicked.connect(self.update_table)

        # Table 2
        self.prediction_result = QtWidgets.QTableWidget(self)
        self.prediction_result.setGeometry(5, 500, 480, 360)
        self.prediction_result.setColumnCount(5)
        self.prediction_result.setRowCount(self.showing_days)
        results = ['timestamp','Index_Code','Index','Action_Code','Buy_or_Sell']
        self.prediction_result.setHorizontalHeaderLabels(results)
        self.update_result()

        # Matplotlib chart
        self.figure = plt.figure(figsize=(7, 4))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.plot_widget = QWidget(self)
        self.plot_widget.setGeometry(740, 120, 720, 360)
        self.plot_widget.setLayout(layout)
        self.update_chart()

        # Order table
        self.order_table = QtWidgets.QTableWidget(self)
        self.order_table.setGeometry(500, 500, 240, 240)
        self.order_table.setColumnCount(0)
        self.order_table.setRowCount(5)
        results = ['Trading_Pair', 'Price(USDT)', 'Buy/Sell','Number','Information Return']
        self.order_table.setVerticalHeaderLabels(results)
        self.param_name = QtWidgets.QLineEdit()
        self.param_price = QtWidgets.QLineEdit()
        self.param_action = QtWidgets.QLineEdit()
        self.param_trade_num = QtWidgets.QLineEdit()
        self.info_return = QtWidgets.QLineEdit()
        
        
        self.order_table.insertColumn(0)
        self.order_table.setCellWidget(0, 0, self.param_name)
        self.order_table.setCellWidget(1, 0, self.param_price)
        self.order_table.setCellWidget(2, 0, self.param_action)
        self.order_table.setCellWidget(3, 0, self.param_trade_num)
        self.order_table.setCellWidget(4, 0, self.info_return)
        
        
        # Buy/Sell buttons
        self.buy_button = QtWidgets.QPushButton('BUY', self)
        self.sell_button = QtWidgets.QPushButton('SELL', self)
        self.buy_button.setGeometry(750, 500, 90, 30)
        self.sell_button.setGeometry(850, 500, 90, 30)
        self.buy_button.clicked.connect(self.set_buy)
        self.sell_button.clicked.connect(self.set_sell)
        #取得實實資料
        self.update_button = QtWidgets.QPushButton('Get Real Time Price', self)
        self.update_button.setGeometry(950, 500, 90, 30)
        self.update_button.clicked.connect(self.get_realtime_price)
        
        # Place order button
        self.place_order_button = QtWidgets.QPushButton('Sent_Order', self)
        self.place_order_button.setGeometry(750, 540, 190, 50)
        self.place_order_button.clicked.connect( self.place_order)

    def update_table(self):
        df = pd.read_excel('prediction_result.xlsx')
        last_7_days = df.tail(self.showing_days)
        for row in range(self.showing_days):
            for col, header in enumerate(['timestamp', 'Open', 'High', 'Low', 'Close']):
                item = QTableWidgetItem(str(last_7_days.at[last_7_days.index[row], header]))
                self.table.setItem(row, col, item)

    def update_result(self):
        re = pd.read_excel('prediction_result.xlsx')
        last_7_days = re.tail(self.showing_days)
        self.prediction_result.setRowCount(self.showing_days)
        for row in range(self.showing_days):
            timestamp = last_7_days.at[last_7_days.index[row], 'timestamp']
            action_label = last_7_days.at[last_7_days.index[row], 'Action']
            index_label = last_7_days.at[last_7_days.index[row], 'Index_1']
            if action_label == 1:
                Action = 'BUY'
            elif action_label == 0:
                Action = 'HOLD'
            elif action_label == -1 :
                Action = 'SELL'

            if index_label == 2:
                Index_1 = 'Upward'
            elif index_label == 0:
                Index_1 = 'Flat'
            elif index_label == -2 :
                Index_1 = 'Downward'

            item_timestamp = QTableWidgetItem(str(timestamp))
            item_action_label = QTableWidgetItem(str(action_label))
            item_index_label =  QTableWidgetItem(str(index_label))
            item_index =  QTableWidgetItem(str(Index_1))
            item_action = QTableWidgetItem(str(Action))
            self.prediction_result.setItem(row, 0, item_timestamp)
            self.prediction_result.setItem(row, 1, item_action_label)
            self.prediction_result.setItem(row, 2, item_index_label)
            self.prediction_result.setItem(row, 3, item_index)
            self.prediction_result.setItem(row, 4, item_action)

    def update_chart(self):
        df = pd.read_excel('prediction_result.xlsx')
        last_30_days = df.tail(self.showing_days)
        last_30_days = last_30_days.sort_values(by='timestamp')
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(last_30_days['timestamp'], last_30_days['Open'], label='Open')
        ax.plot(last_30_days['timestamp'], last_30_days['High'], label='High')
        ax.plot(last_30_days['timestamp'], last_30_days['Low'], label='Low')
        ax.plot(last_30_days['timestamp'], last_30_days['Close'], label='Close')
        ax.legend()
        self.canvas.draw()

    def place_order(self):
        symbol = self.param_name.text()
        price = self.param_price.text()
        action = self.param_action.text()
        amount = self.param_trade_num
        re = self.info_return
        binance = ccxt.binance({
            'api_key' : 'tI5stusyJOWv5EQsWeko2PspaJ0KseBVFmSlXimMlkiIiDOyOfj2zpEaPKygrVC6',
            'secret' : 'IWrubycoG3mYssDswLjcqMPW2O5eckDGby6d85g93dBrH7VxwmkBVq4SUZJHXmM8'
            
            })
        if action == 'BUY':
            try:
                order = binance.create_limit_buy_order(symbol, amount, price)
                print("買入訂單詳情：", order)
                re = order
                self.info_return.setText(str(re))

                
            except Exception as e:
                print('Error: Without Permissions')
                re = 'Error: Without Permissions'
                self.info_return.setText(str(re))
                
        elif action == 'SELL':
            try:
                order = binance.create_limit_sell_order(symbol, amount, price)
                print("賣出訂單詳情：", order)
                re = order
                
                self.info_return.setText(str(re))
            except Exception as e:
                print('Error: Without Permissions')
                re = 'Error: Without Permissions'
                self.info_return.setText(str(re))
        else:
            print('Error: Wrong Commend')
            re = 'Error: Wrong Commend'
            self.info_return.setText(str(re))
        
        
        
        


    def set_buy(self):
        action = 'BUY'
        self.param_action.setText(str(action))
    
    def set_sell(self):
        action = 'SELL'
        self.param_action.setText(str(action))


    def get_realtime_price(self):
        symbol = self.param_name.text()
        
        binance = ccxt.binance({
            'api_key' : 'tI5stusyJOWv5EQsWeko2PspaJ0KseBVFmSlXimMlkiIiDOyOfj2zpEaPKygrVC6',
            'secret' : 'IWrubycoG3mYssDswLjcqMPW2O5eckDGby6d85g93dBrH7VxwmkBVq4SUZJHXmM8'
            
            })
        print(symbol)
        ticker = binance.fetch_ticker(symbol)
        price = ticker['last']
        print(f"The current price of {symbol} is {price} USDT.")
        self.order_table.setItem(0, 1, QtWidgets.QTableWidgetItem(str(price)))
        try:
            self.param_price.setText(str(price))  # 将价格填回表格中的 "Price(USDT)" 栏位
        except Exception as e:
            print(f"Error fetching price for {symbol}: {e}")





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = sub_page1_information_table()
    window.show()
    sys.exit(app.exec_())
    app.quit()  
        
        
        

    