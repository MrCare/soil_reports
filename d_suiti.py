'''
Author: Mr.Car
Date: 2024-06-21 15:12:58
'''
import os
from inner import QUAL_74, QUAL_72, SUITI_64, SUITI_67, SUITI_71, SUITI_167, SUITI_66
from alive_progress import alive_bar
from inner.share import *
from inner.load_config import ConfigLoader

config_loader = ConfigLoader()
yaml_data = config_loader.yaml
csv_data = config_loader.csv
inner_xls_template_path = config_loader.inner_xls_template_path

def type_56(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    # 测试数据中暂时没有 SUITI_165
    type_74_for_suti_list = ['SUITI_56','SUITI_57','SUITI_58','SUITI_59','SUITI_60','SUITI_61','SUITI_164','SUITI_166','SUITI_63']
    total_steps = len(type_74_for_suti_list) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="56-63:适宜性评价等级分布:") as bar:
        for sheet_name in type_74_for_suti_list:
            df = read_and_prepare_file(file_pth)
            wb = get_wb(xls_template_path)
            wb = QUAL_74.statistics_all(df, csv_data, yaml_data, wb, bar, sheet_name)
            save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_62(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="62:宜类评价面积表:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_72.statistics_all(df, yaml_data, wb, bar, 'SUITI_62')
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_64(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    sheet_name_list = ['SUITI_64', 'SUITI_65']
    total_steps = len(sheet_name_list) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="64-65:土类亚类及适宜程度面积表:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        for sheet_name in sheet_name_list:
            wb = SUITI_64.statistics_all(df, yaml_data, wb, bar, sheet_name)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_67(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    sheet_name_list = ['SUITI_67', 'SUITI_68', 'SUITI_69', 'SUITI_70']
    total_steps = len(sheet_name_list) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="67-70:地类面积错配表:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        for sheet_name in sheet_name_list:
            wb = SUITI_67.statistics_all(df, yaml_data, wb, bar, sheet_name)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_71(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="71:耕地后备资源面积表:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = SUITI_71.statistics_all(df, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_167(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="167:限制因素等级表:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = SUITI_167.statistics_all(df, csv_data, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_66(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="66:适宜类面积:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = SUITI_66.statistics_all(df, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def suiti(suti_pth, out_file_pth=None, xls_template_path=inner_xls_template_path):
    type_56(suti_pth, xls_template_path, out_file_pth)
    type_62(suti_pth, out_file_pth, out_file_pth)
    type_64(suti_pth, out_file_pth, out_file_pth)
    type_67(suti_pth, out_file_pth, out_file_pth)
    type_71(suti_pth, out_file_pth, out_file_pth)
    type_167(suti_pth, out_file_pth, out_file_pth)
    type_66(suti_pth, out_file_pth, out_file_pth)

if __name__ == "__main__":
    # type_167("/Users/car/Work/2023workPlan/三普土壤制图工具/测试与新需求/0617/样例数据0617/适宜性评价.shp")
    type_64("/Users/car/Project/soilCli/reports/test_data/suiti_result/suiti_result_short.shp")