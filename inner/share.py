'''
Author: Mr.Car
Date: 2024-02-29 18:13:50
'''
import pandas as pd
import os
import yaml

class ConfigLoader:
    '''
    载入配置文件
    '''
    def __init__(self, folder_path):
        self.yaml = {}
        self.csv = {}
        self.load_cfg_files(folder_path)

    def load_cfg_files(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith('.yaml'):
                    with open(os.path.join(root, filename), 'r') as f:
                        data = yaml.load(f, Loader=yaml.FullLoader)
                        self.yaml.update(data)
                if filename.endswith('.csv'):
                    file_path = os.path.join(root, filename)  # 获取文件的完整路径
                    dataframe = pd.read_csv(file_path)  # 读取 CSV 文件为 Pandas DataFrame
                    dataframe.set_index('name', inplace=True)
                    self.csv[os.path.splitext(filename)[0]] = dataframe # 使用文件名（不包含扩展名）作为字典的键，并将 DataFrame 存储为值

def fill_template(sheet, start_position, value_list, horizon=True):
    start_row, start_col = int(start_position[1:]), ord(start_position[0].upper()) - 64 # B4 转为 列标数字
    for each in value_list:
        sheet.cell(row=start_row, column=start_col, value=each)
        if horizon:
            start_col += 1
        else:
            start_row += 1
    return sheet

def fill_title(sheet, title, position="A1"):
    sheet[position] = title 
    return sheet

def fill_value(sheet, value, position):
    sheet[position] = value
    return sheet

def get_sheet(wb, template):
    sheet_name = next(x for x in wb.sheetnames if template in x)
    sheet = wb[sheet_name]
    return sheet