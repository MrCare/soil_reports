'''
Author: Mr.Car
Date: 2024-01-07 17:34:41
'''
import pandas as pd
import geopandas as gpd
import os
import fire
import warnings

from inner import *
from alive_progress import alive_bar
from openpyxl import load_workbook

# 忽略 FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# 指定包含 CSV 文件的文件夹路径
folder_path = os.path.join(os.path.dirname(__file__), 'config')
xls_template_path = os.path.join(folder_path, 'cfg_template.xlsx')


# 载入配置文件
csv_data = {}
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)  # 获取文件的完整路径
        dataframe = pd.read_csv(file_path)  # 读取 CSV 文件为 Pandas DataFrame
        dataframe.set_index('name', inplace=True)
        csv_data[os.path.splitext(filename)[0]] = dataframe # 使用文件名（不包含扩展名）作为字典的键，并将 DataFrame 存储为值

cfg_index = csv_data['cfg_index']

def get_cfg_params(cfg_index, name):
    var_table = csv_data[cfg_index.loc[name]["var"]]
    rule_table = csv_data[cfg_index.loc[name]["rule"]]
    field = cfg_index.loc[name]["field"]
    title = cfg_index.loc[name]["title"]
    nan_filler = cfg_index.loc[name]["nan_filler"]
    return var_table, rule_table, field, title, nan_filler

def get_sheet(xls_file_path, template):
    wb = load_workbook(xls_file_path)    
    sheet_name = next(x for x in wb.sheetnames if template in x)
    sheet = wb.get_sheet_by_name(sheet_name)
    return wb, sheet

def fill_title(sheet, title, position="A1"):
    sheet[position] = title
    return sheet

def fill_template(sheet, position, value):
    sheet[position] = value
    return sheet

def deal_none(df, field, rule_table):
    '''
    输入样点数据 输出df(除了空值之外的) 输出df(空值)
    '''
    ss = df[field]
    rule_str = rule_table.loc["none"]["value"]
    ss_none = ss[ss.apply(lambda x: eval(rule_str, {"x": x}))]
    ss_not_none = ss[ss.apply(lambda x: not eval(rule_str, {"x": x}))]
    return ss_none, ss_not_none

def save_xls(wb, xls_file_path):
    wb.save(xls_file_path)
    return

def get_var(ss, rule_table, classification, method, nan_filler):
    '''
    '''
    rule_str = rule_table.loc[classification]['value']
    ss_result = ss[ss.apply(lambda x: eval(rule_str, {"x": x}))]
    result = None
    if method == "mean":
        mean_value = ss_result.mean()
        result = nan_filler if pd.isna(mean_value)  else "{:.2f}%".format(mean_value) # 均值保留两位小数, 如果无法算均值填充 “/”
    elif method == "count":
        result = ss_result.count()
    elif method == "percent":
        result = "{:.2f}%".format( (ss_result.count() / ss.count()) * 100 ) # 保留两位小数百分数
    return result

def statistics_all(ss, var_table, rule_table, sheet, nan_filler):
    wb = None
    for var, row in var_table.iterrows():
        classification = row["classification"]
        method = row["method"]
        position = row["position"]
        var_result = get_var(ss, rule_table, classification, method, nan_filler)
        fill_template(sheet, position, var_result)
    return

def main(file_pth, name, out_file_pth=None):
    total_steps = 1
    with alive_bar(total_steps) as bar:
        df = gpd.read_file(file_pth)
        var_table, rule_table, field, title, nan_filler = get_cfg_params(cfg_index, name)
        wb, sheet = get_sheet(xls_template_path, name)
        sheet = fill_title(sheet,title,"A1")
        ss_none, ss_not_none = deal_none(df, field, rule_table)
        statistics_all(ss_not_none, var_table, rule_table, sheet, nan_filler)
        if not out_file_pth:
            out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xls')
        save_xls(wb, out_file_pth)
    bar()
    return "Done!"

if __name__ == "__main__":
    # main('./test_data/表层样点.shp', 'JSBG_7_PH')
    fire.Fire(main)