# -*- coding: utf-8 -*-
"""
Created on Wed May 29 19:01:46 2024

@author: pgn63
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:08:24 2024

@author: pgn63
"""

import sys
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt,pyqtSignal,pyqtSlot
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pandas as pd
from K_Line_History import GUI_backtest_get_data
from crypto_prediction_sub import run_daily_routine
from randam_backtest_program import run_backtest
class sub_page2_information_table(QMainWindow):
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

        # 设置暗色系主题
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c2c2c;
            }
            QLabel {
                color: white;
            }
            QTableWidget {
                background-color: white;
                color: white;
                gridline-color: white;
            }
            QPushButton {
                background-color: #424242;
                color: white;
                border: 1px solid white;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)

        # 标题标签
        self.title_label = QLabel("Trading Informations and Parameters Settings")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        self.layout.addWidget(self.title_label)

        #說明標籤
        self.commentary_label = QLabel('Using Guide - Default Example')
        self.commentary_label.setAlignment(Qt.AlignCenter)
        self.commentary_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.layout.addWidget(self.commentary_label)
        self.commentary_content = QLabel(
            'symbol = BTC/USDT '
            'timeframe = 1d '
            'start_date = 2023-01-01T00:00:00Z ''end_date = 2023-12-31T00:00:00Z \n'
            'output_path = ALTCOIN歷史資料.xlsx '
            'data_path = ALTCOIN歷史資料.xlsx '
            'check_symbol = BTC-USD\n '
            'prediction_result = prediction_result.xlsx '
            'check_prediction_result = prediction_result_v2_check.xlsx '
            'year = 2024 '
            'prediction_result = prediction_result.xlsx '
            )
        self.commentary_content.setAlignment(Qt.AlignCenter)
        self.commentary_content.setStyleSheet("font-weight: bold; font-size: 16px; border: 2px solid #D8BFD8;")
        self.layout.addWidget(self.commentary_content)
        # 表格和小标题
        self.add_table_with_title("Get Historical Data Parameters", ["symbol", "timeframe", "start_date", "end_date", 'output_path'])
        self.add_table_with_title("Run Prediction Parameters", ["data_path", "check_symbol", 'prediction_result', 'check_prediction_result'])
        self.add_table_with_title("Back Testing Parameters", ["year", 'prediction_result'])
        

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

    def add_table_with_title(self, title, headers):
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        self.layout.addWidget(title_label)

        table = QTableWidget(1, len(headers))
        table.setHorizontalHeaderLabels(headers)
        self.layout.addWidget(table)
        

        
        
    def crypto_function(self):
        print("Crypto button clicked")
        
        
        
        
        symbol = []
        timeframe = []
        start_date = []
        end_date = []
        output_path = []
        
        data_path = []
        check_symbol = []
        prediction_result = []
        check_prediction_result = []
        
        year = []
        prediction_result = []
        
        try:
            for row in range(self.table.rowCount()):
                symbol.append(self.table.item(row, 0).text())
                timeframe.append(self.table.item(row, 1).text())
                start_date.append(self.table.item(row, 2).text())
                end_date.append(self.table.item(row, 3).text())
                output_path.append(self.table.item(row, 4).text())
        except Exception as e:
            print('No settings. Using default values.')
        try:    
            for row in range(self.table2.rowCount()):
                data_path.append(self.table2.item(row, 0).text())
                check_symbol.append(self.table2.item(row, 1).text())
                prediction_result.append(self.table2.item(row, 2).text())
                check_prediction_result.append(self.table2.item(row, 3).text())
        except Exception as e:
            print('No settings. Using default values.')
        try:
            for row in range(self.table2.rowCount()):
                year.append(self.table2.item(row, 0).text())
                prediction_result.append(self.table2.item(row, 1).text())
        except Exception as e:
            print('No settings. Using default values.')   

        try:
            symbol = ", ".join([self.table.item(row, 0).text() for row in range(self.table.rowCount())])
            timeframe = ", ".join([self.table.item(row, 1).text() for row in range(self.table.rowCount())])
            start_date = ", ".join([self.table.item(row, 2).text() for row in range(self.table.rowCount())])
            end_date = ", ".join([self.table.item(row, 3).text() for row in range(self.table.rowCount())])
            output_path = ", ".join([self.table.item(row, 4).text() for row in range(self.table.rowCount())])
            
            data_path = ", ".join([self.table2.item(row, 0).text() for row in range(self.table2.rowCount())])
            check_symbol = ", ".join([self.table2.item(row, 1).text() for row in range(self.table2.rowCount())])
            prediction_result = ", ".join([self.table2.item(row, 2).text() for row in range(self.table2.rowCount())])
            check_prediction_result = ", ".join([self.table2.item(row, 3).text() for row in range(self.table2.rowCount())])
            
            year = ", ".join([self.table3.item(row, 0).text() for row in range(self.table3.rowCount())])
            prediction_result = ", ".join([self.table3.item(row, 1).text() for row in range(self.table3.rowCount())])
        except Exception as e:
            """設定預設值"""
            symbol = 'BTC/USDT'
            timeframe = '1d'
            start_date = '2023-01-01T00:00:00Z'
            end_date = '2023-12-31T00:00:00Z'
            output_path = 'ALTCOIN歷史資料.xlsx'
            data_path = 'ALTCOIN歷史資料.xlsx'
            check_symbol = 'BTC-USD'
            prediction_result = 'prediction_result.xlsx'
            check_prediction_result = 'prediction_result_v2_check.xlsx'
            year = 2024
            prediction_result = 'prediction_result.xlsx'   
        


        GUI_backtest_get_data(symbol,timeframe,start_date,end_date,output_path)

        run_daily_routine(symbol,
                          timeframe, 
                          data_path, 
                          check_symbol,
                          prediction_result,
                          check_prediction_result,
                          )
        run_backtest(prediction_result,year)
        
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
        self.order_table.setGeometry(500, 500, 240, 180)
        self.order_table.setColumnCount(0)
        self.order_table.setRowCount(3)
        results = ['Trading_Pair', 'Price(USDT)', 'Buy/Sell']
        self.order_table.setVerticalHeaderLabels(results)
        self.param_name = QtWidgets.QLineEdit()
        self.param_price = QtWidgets.QLineEdit()
        self.order_table.insertColumn(0)
        self.order_table.setCellWidget(0, 0, self.param_name)
        self.order_table.setCellWidget(1, 0, self.param_price)

        # Buy/Sell buttons
        self.buy_button = QtWidgets.QPushButton('BUY', self)
        self.sell_button = QtWidgets.QPushButton('SELL', self)
        self.buy_button.setGeometry(750, 500, 90, 30)
        self.sell_button.setGeometry(850, 500, 90, 30)
        self.buy_button.clicked.connect(lambda: self.set_buy_sell('BUY'))
        self.sell_button.clicked.connect(lambda: self.set_buy_sell('SELL'))

        # Place order button
        self.place_order_button = QtWidgets.QPushButton('Sent_Order', self)
        self.place_order_button.setGeometry(750, 540, 190, 50)
        self.place_order_button.clicked.connect(self.place_order)

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
        trading_pair = self.param_name.text()
        price = self.param_price.text()
        print(f'下單成功: {trading_pair}, 價格: {price}')
        self.place_order_button.setText('Order_Sented')

    def set_buy_sell(self, action):
        self.order_table.item(2, 0).setText(action)

    







if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = sub_page2_information_table()
    window.show()
    sys.exit(app.exec_())
    app.quit()  
        
        
        