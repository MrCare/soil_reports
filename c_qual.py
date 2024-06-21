'''
Author: Mr.Car
Date: 2024-06-21 15:12:50
'''
import os
from inner import QUAL_76_78, QUAL_77, QUAL_72, QUAL_73, QUAL_74, QUAL_75
from alive_progress import alive_bar
from inner.share import *
from inner.load_config import ConfigLoader

config_loader = ConfigLoader()
yaml_data = config_loader.yaml
csv_data = config_loader.csv
inner_xls_template_path = config_loader.inner_xls_template_path

def batch_type_76(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    var_table = csv_data['cfg_76and78_var']
    total_steps = len(var_table) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="76-106:土壤质量等级面积与产能分布:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_76_78.statistics_all(df, var_table, csv_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def batch_type_77(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    var_table = csv_data['cfg_77_var']
    total_steps = len(var_table) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="77-107:土壤质量属性情况:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_77.statistics_all(df, var_table, csv_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_72(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="72:土壤质量等级面积及其占比:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_72.statistics_all(df, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"


def type_73(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="73:土壤质量等级及得分:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_73.statistics_all(df, csv_data, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_74(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None, sheet_name="QUAL_74"):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="74:耕地质量等级面积总分布:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_74.statistics_all(df, csv_data, yaml_data, wb, bar, sheet_name)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"


def type_75(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="75:各街道耕地产能:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_75.statistics_all(df, csv_data, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def qual(qual_pth, out_file_pth=None, xls_template_path=inner_xls_template_path):
    type_72(qual_pth, xls_template_path, out_file_pth)
    type_73(qual_pth, out_file_pth, out_file_pth)
    type_74(qual_pth, out_file_pth, out_file_pth)
    type_75(qual_pth, out_file_pth, out_file_pth)
    batch_type_76(qual_pth, out_file_pth, out_file_pth)
    batch_type_77(qual_pth, out_file_pth, out_file_pth)