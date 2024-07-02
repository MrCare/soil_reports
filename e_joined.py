'''
Author: Mr.Car
Date: 2024-07-02 09:59:13
'''
import os
from inner import JSBG_13, JSBG_14
from alive_progress import alive_bar
from inner.share import *
from inner.load_config import ConfigLoader

config_loader = ConfigLoader()
yaml_data = config_loader.yaml
csv_data = config_loader.csv
inner_xls_template_path = config_loader.inner_xls_template_path
cfg_index = config_loader.cfg_index


def type_13(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    sheet_list = ["JSBG_013", "JSBG_015"]
    total_steps = len(sheet_list) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="13&15:样点土壤质地统计:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        for each in sheet_list:
            wb = JSBG_13.statistics_all(df, yaml_data, wb, bar, each)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_14(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="14:样点颗粒组成统计:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = JSBG_14.statistics_all(df, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def joined(file_pth, out_file_pth=None, xls_template_path=inner_xls_template_path):
    type_13(file_pth, inner_xls_template_path, out_file_pth)
    type_14(file_pth, out_file_pth, out_file_pth)