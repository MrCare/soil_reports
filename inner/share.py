'''
Author: Mr.Car
Date: 2024-02-29 18:13:50
'''
import pandas as pd
import os
import yaml
import openpyxl


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
                    with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                        data = yaml.load(f, Loader=yaml.FullLoader)
                        self.yaml.update(data)
                if filename.endswith('.csv'):
                    file_path = os.path.join(root, filename)  # 获取文件的完整路径
                    dataframe = pd.read_csv(file_path)  # 读取 CSV 文件为 Pandas DataFrame
                    dataframe.set_index('name', inplace=True)
                    self.csv[os.path.splitext(filename)[0]] = dataframe # 使用文件名（不包含扩展名）作为字典的键，并将 DataFrame 存储为值

class XlsPosUtil:
    '''
    处理 excel 中的 position 字符串
    '''
    def __init__(self, position=""):
        if position:
            self.position = position
            self.start_row, self.start_col = int(position[1:]), ord(position[0].upper()) - 64 # B4 转为 列标数字
    def get_row_col(self, position):
        row, col = int(position[1:]), ord(position[0].upper()) - 64 # B4 转为 列标数字
        return row, col

    def get_excel_position(self, row, col):
        '''
        openpyxl 没有直接提供转换函数，但可以使用 get_column_letter 函数来获取列的字母表示，然后拼接行号;
        4,1 -> A4        
        '''
        # openpyxl 没有直接提供转换函数，但可以使用 get_column_letter 函数
        # 来获取列的字母表示，然后拼接行号。
        col_letter = openpyxl.utils.get_column_letter(col)
        return f"{col_letter}{row}"

    def position_add_row(self, position, num):
        row, col = self.get_row_col(position)
        row += num
        return self.get_excel_position(row, col)

    def _position_add_col(self, position, num):
        row, col = self.get_row_col(position)
        col += num
        return self.get_excel_position(row, col)

    def segment(self, result_list, start_position, seg_length, position_interval, horizon=True):
        '''
        处理数据过长时候的分行显示问题
        [1,2,3,4] -> [1,2,3][4]
        '''
        start_row, start_col = self.get_row_col(start_position)
        position_list = []
        group_result_list = []
        groups = len(result_list) // seg_length
        for i in range(groups):
            group_result_list.append(result_list[seg_length*i : seg_length*(i+1)])
            if horizon:
                start_row += i * position_interval
            else:
                start_col += i * position_interval
            position_list.append(self.get_excel_position(start_row, start_col))
        return position_list, group_result_list
    

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