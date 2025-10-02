# -*- coding: utf-8 -*-
"""
Created on Tue May 28 12:23:37 2024

@author: pgn63
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap

from subpage_settings import sub_page1_information_table
from backtest_settings import sub_page2_information_table
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 800, 600)

        # 主 widget 和布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)
        
        
        # Background image
        # 设置背景图片
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, 10000, 6000)
        background_pixmap = QPixmap('背景.jpg')
        self.background_label.setPixmap(background_pixmap)
        self.background_label.lower()
        self.background_label.setStyleSheet("background-image: url('背景.jpg'); background-size: cover;")
        
        # QStackedWidget 来切换不同页面
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # 封面页面
        self.cover_page = QWidget()
        self.cover_layout = QVBoxLayout(self.cover_page)

        # 添加标题
        self.title_label = QLabel("AI-Driven Automated System in Cryptocurrency Trading GUI")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white; font-weight: bold; font-size: 24px;")
        self.cover_layout.addWidget(self.title_label)

        # 添加图片（假设你有一个名为 image_label 的 QLabel 用于显示图片）
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.cover_layout.addWidget(self.image_label)

        """添加按钮到封面页面"""
        self.button1 = QPushButton("Real Time Testing")
        self.button2 = QPushButton("Back Testing")
        self.button3 = QPushButton("Others")

        self.button1.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page1))
        self.button2.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page2))
        self.button3.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.page3))

        # 使用 QVBoxLayout 将按钮垂直排列
        self.button_layout = QVBoxLayout()
        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)
        self.cover_page.setLayout(self.button_layout)
        # 添加按钮布局到封面布局
        self.cover_layout.addLayout(self.button_layout)

        # 添加封面页面到 QStackedWidget
        self.stacked_widget.addWidget(self.cover_page)


        
        # 添加子页面到 QStackedWidget
        self.page1 = sub_page1_information_table()
        self.stacked_widget.addWidget(self.page1)

        # 功能页面2
        self.page2 = sub_page2_information_table()
        self.stacked_widget.addWidget(self.page2)

        # 功能页面3
        self.page3 = QWidget()
        self.page3_layout = QVBoxLayout(self.page3)
        self.page3_label = QPushButton("这是功能 3 的页面")
        self.page3_layout.addWidget(self.page3_label)
        self.stacked_widget.addWidget(self.page3)

        # 显示封面页面
        self.stacked_widget.setCurrentWidget(self.cover_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    app.quit()
