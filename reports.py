# -*- coding: utf-8 -*-

'''
Author: Mr.Car
Date: 2024-01-07 17:34:41
'''
import pandas as pd
import numpy as np
import geopandas as gpd
import os
import fire
import warnings

from inner import JSBG_7, JSBG_8, TRSX_111, TRSX_112, zonal_statistics, check
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

def read_and_prepare_file(file_pth):
    df = gpd.read_file(file_pth)
    # df.replace({np.nan: None}, inplace=True)
    return df

def get_cfg_params(cfg_index, name, result_type="variable"):
    if result_type == "variable":
        var_table = csv_data[cfg_index.loc[name]["var"]]
    if result_type == "file_pth":
        var_table = os.path.join(folder_path, cfg_index.loc[name]["var"])
    rule_table = csv_data[cfg_index.loc[name]["rule"]]
    field = cfg_index.loc[name]["field"]
    target_field = cfg_index.loc[name]["target_field"]
    title = cfg_index.loc[name]["title"]
    nan_filler = cfg_index.loc[name]["nan_filler"]
    return var_table, rule_table, field, target_field, title, nan_filler

def get_wb(xls_file_path):
    wb = load_workbook(xls_file_path)    
    return wb

def get_sheet(wb, template):
    sheet_name = next(x for x in wb.sheetnames if template in x)
    sheet = wb[sheet_name]
    return sheet

def fill_title(sheet, title, position="A1"):
    sheet[position] = title 
    return sheet

def fill_value(sheet, value, position):
    sheet[position] = value
    return sheet

def fill_column_title(var_table, sheet):
    '''
    填充标题列
    '''
    for name, row in var_table.iterrows():
        locate_position = row["locate_position"]
        title = row["title"]
        if not pd.isna(locate_position) and not pd.isna(title):
            sheet = fill_value(sheet, title, locate_position)
    return sheet

def deal_none(df, field, rule_table, result_type="ss"):
    '''
    输入样点数据 输出df(除了空值之外的) 输出df(空值)
    '''
    ss = df[field]
    rule_str = rule_table.loc["none"]["value"]
    ss_none = ss[ss.apply(lambda x: eval(rule_str, {"x": x}))]
    df_none = df[ss.apply(lambda x: eval(rule_str, {"x": x}))]
    ss_not_none = ss[ss.apply(lambda x: not eval(rule_str, {"x": x}))]
    df_not_none = df[ss.apply(lambda x: not eval(rule_str, {"x": x}))]
    if result_type == "ss":
        return ss_none, ss_not_none
    elif result_type == "df":
        return df_none, df_not_none

def save_xls(wb, xls_file_path):
    wb.save(xls_file_path)
    return

def prepare_cfg(origin_file_pth, cfg_name, parent_field):
    '''
    准备好文件
    '''
    with alive_bar(1, title="生成配置文件:") as bar:
        TRSX_112.prepare(origin_file_pth, folder_path, cfg_name, parent_field)
        bar()
    return "Done!"

def batch_type_7(file_pth, table_list, xls_template_path=xls_template_path, out_file_pth=None):
    total_steps = len(table_list) + 1
    with alive_bar(total_steps, title="表层样数据分析:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        for table in table_list:
            var_table, rule_table, field, target_field, title, nan_filler = get_cfg_params(cfg_index, table)
            sheet = get_sheet(wb, table)
            sheet = fill_title(sheet, title, "A1")
            ss_none, ss_not_none = deal_none(df, field, rule_table)
            JSBG_7.statistics_all(ss_not_none, var_table, rule_table, sheet, nan_filler)
            if not out_file_pth:
                out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
            bar()

        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def batch_type_111(file_pth, table_list, xls_template_path=xls_template_path, out_file_pth=None):
    total_steps = len(table_list) + 1
    with alive_bar(total_steps, title="评价单元数据分析:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        for table in table_list:
            var_table, rule_table, field, target_field, title, nan_filler = get_cfg_params(cfg_index, table)
            sheet = get_sheet(wb, table)
            sheet = fill_title(sheet, title, "A1")
            sheet = fill_column_title(var_table, sheet)
            df_none, df_not_none = deal_none(df, field, rule_table, 'df')
            df = TRSX_111.prepare(df_not_none)
            TRSX_111.statistics_all(df, field, target_field, var_table, rule_table, sheet, nan_filler)
            if not out_file_pth:
                out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
            bar()

        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def batch_type_8(file_pth, table_list, xls_template_path=xls_template_path, out_file_pth=None):
    total_steps = len(table_list) + 1
    with alive_bar(total_steps,title="评价单元数据分析:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        for table in table_list:
            var_table, rule_table, field, target_field, title, nan_filler = get_cfg_params(cfg_index, table)
            sheet = get_sheet(wb, table)
            sheet = fill_title(sheet, title, "A1")
            df_none, df_not_none = deal_none(df, field, rule_table, 'df')
            JSBG_8.statistics_all(df_not_none, field, target_field, var_table, sheet, nan_filler)
            if not out_file_pth:
                out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
            bar()
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def quality_check(shp, shp_type="sample"):
    global_rule_file = os.path.join(folder_path, 'cfg_check_rule_all.csv')
    sample_rule_file = os.path.join(folder_path, 'cfg_check_rule_sample.csv')
    element_rule_file = os.path.join(folder_path, 'cfg_check_rule_element.csv')
    output_file = os.path.join(os.path.dirname(shp), os.path.splitext(os.path.basename(shp))[0] + '_check_results.csv')
    if shp_type == 'sample':
        check.quality_check(global_rule_file, [shp], output_file, [sample_rule_file])
    elif shp_type == "element":
        check.quality_check(global_rule_file, [shp], output_file, [element_rule_file])
    else:
        check.quality_check(global_rule_file, [shp], output_file)
    return "Done!"

def total(sample_pth, element_pth, type_list, out_file_pth=None):
    xls_template_path = os.path.join(os.path.dirname(sample_pth), 'reports_result.xlsx')
    type_7_list = [
        'JSBG_7_PH',
        'JSBG_10_OM',
        'JSBG_16_TN',
        'JSBG_19_TP',
        'JSBG_22_TK',
        'JSBG_25_AP',
        'JSBG_28_AK',
        'JSBG_31_AS1',
        'JSBG_34_AFE',
        'JSBG_37_AMN',
        'JSBG_40_ACU',
        'JSBG_43_AZN',
        'JSBG_46_AB',
        'JSBG_49_AMO',
        'JSBG_53_GZCHD'
        ]
    type_111_list = [
        'TRSX_111_PH',
        'TRSX_112_PH',
        'TRSX_113_PH',
        'TRSX_114_CEC',
        'TRSX_115_CEC',
        'TRSX_116_CEC',
        'TRSX_117_TRRZPJZ',
        'TRSX_118_TRRZPJZ',
        'TRSX_119_TRRZPJZ',
        'TRSX_120_GZCHD',
        'TRSX_121_GZCHD',
        'TRSX_122_GZCHD',
        'TRSX_123_TRZD',
        'TRSX_124_TRZD',
        'TRSX_125_TRZD',
        'TRSX_126_TRSL',
        'TRSX_127_TRSL',
        'TRSX_128_TRSL',
        'TRSX_129_TRFSL',
        'TRSX_130_TRFSL',
        'TRSX_131_TRFSL',
        'TRSX_132_TRNL',
        'TRSX_133_TRNL',
        'TRSX_134_TRNL',
        'TRSX_135_OM',
        'TRSX_136_OM',
        'TRSX_137_OM',
        'TRSX_138_TN',
        'TRSX_139_TN',
        'TRSX_140_TN',
        'TRSX_141_TP',
        'TRSX_142_TP',
        'TRSX_143_TP',
        'TRSX_144_TK',
        'TRSX_145_TK',
        'TRSX_146_TK',
        'TRSX_147_AP',
        'TRSX_148_AP',
        'TRSX_149_AP',
        'TRSX_150_AK',
        'TRSX_151_AK',
        'TRSX_152_AK'
        ]
    type_8_list = [
        'JSBG_8_PH',
        'JSBG_11_OM',
        'JSBG_17_TN',
        'JSBG_20_TP',
        'JSBG_23_TK',
        'JSBG_26_AP',
        'JSBG_29_AK',
        'JSBG_32_AS1',
        'JSBG_35_AFE',
        'JSBG_38_AMN',
        'JSBG_41_ACU',
        'JSBG_44_AZN',
        'JSBG_47_AB',
        'JSBG_50_AMO',
        'JSBG_54_GZCHD'
        ]
    for each in type_list:
        if each == "JSBG_7":
            batch_type_7(sample_pth, type_7_list)
        elif each == "TRSX_111":
            # batch_type_111(element_pth, ['TRSX_111_PH', 'TRSX_135_OM', 'TRSX_114_CEC', 'TRSX_117_TRRZPJZ', 'TRSX_120_GZCHD', 'TRSX_123_TRZD', 'TRSX_126_TRSL', 'TRSX_129_TRFSL', 'TRSX_132_TRNL', 'TRSX_138_TN', 'TRSX_141_TP', 'TRSX_144_TK', 'TRSX_147_AP', 'TRSX_150_AK'], xls_template_path)
            batch_type_111(element_pth, type_111_list, xls_template_path)
        elif each == "JSBG_8":
            batch_type_8(element_pth, type_8_list, xls_template_path)
        else:
            print('ERROR!')
    return "Done!"

if __name__ == "__main__":
    '''
    reports batch_type_7 --file_pth ./test_data/表层样点.shp --table_list "[JSBG_7_PH,JSBG_8_OM]"--out_file_pth xx.shp
    reports batch_type_111 --file_pth xx.shp --table_list "[JSBG_7_PH]" --out_file_pth xx.shp
    python reports.py quality_check --shp_files "['./test_data/表层样点.shp']"
    '''
    # zonal_statistics.zs('./test_data/PH评价单元.shp','./test_data/OM预测.tif','OM','./test_data/PH_OM评价单元.shp')
    # batch_type_7('./test_data/表层样点.shp', ['JSBG_7_PH','JSBG_10_OM','JSBG_16_TN','JSBG_19_TP','JSBG_22_TK','JSBG_25_AP','JSBG_28_AK','JSBG_31_AS1','JSBG_34_AFE','JSBG_37_AMN','JSBG_40_ACU','JSBG_43_AZN','JSBG_46_AB','JSBG_49_AMO','JSBG_53_GZCHD'])
    # batch_type_111('./test_data/评价单元.shp', ['TRSX_117_TRRZPJZ'])
    
    # 生成配置文件

    prepare_cfg('./test_data/评价单元.shp','cfg_112_var','XZQMC')
    prepare_cfg('./test_data/评价单元.shp','cfg_113_var','TL')

    # batch_type_111('./test_data/PH_OM评价单元.shp', ['TRSX_112_PH', 'TRSX_113_PH'])
    # batch_type_8('./test_data/评价单元.shp', ['JSBG_8_PH'])
    quality_check("./test_data/表层样点.shp", shp_type='sample')
    quality_check('./test_data/评价单元.shp', shp_type='element')
    # total('./test_data/表层样点.shp', './test_data/评价单元.shp', [
    #     'JSBG_7',
    #     'JSBG_8',
    #     'TRSX_111'
    # ])

    # fire.Fire({
    #     "zs": zonal_statistics.zs,
    #     "total": total,
    #     "get_var_table": prepare_cfg,
    #     "quality_check": quality_check,
    #     "batch_type_7": batch_type_7,
    #     "batch_type_111": batch_type_111,
    # })