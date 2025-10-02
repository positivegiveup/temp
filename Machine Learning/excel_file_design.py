# -*- coding: utf-8 -*-
"""
Created on Wed Jan 24 14:57:47 2024

@author: pgn63
"""

import pandas as pd

def table_design(result_file):
    predictions_result = pd.read_excel(result_file)
    predictions_result.to_excel(result_file, index=True)

    # 使用 xlsxwriter 写入 Excel 文件
    with pd.ExcelWriter(result_file, engine='xlsxwriter') as writer:
        predictions_result.to_excel(writer, index=True, sheet_name='Sheet1')

        # 獲取 xlsxwriter workbook 和 worksheet 對象
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        # 添加條件格式
        icon_set_format = workbook.add_format({
            'type': 'icon_set',
            'icon_set': '3_traffic_lights',
            'icons': [{'criteria': '>=', 'type': 'number', 'value': 0},
                      {'criteria': '<', 'type': 'number', 'value': 0}]
        })

        # 將條件格式應用於整個 'Predicted' 列
        worksheet.conditional_format('C2:C100', {'type': 'icon_set',
                                                 'icon_set': '3_traffic_lights',
                                                 'icons': [{'criteria': '>=', 'type': 'number', 'value': 0},
                                                           {'criteria': '<', 'type': 'number', 'value': 0}]})

# 调用子程序，传递 result_file 参数
table_design('your_result_file.xlsx')

    