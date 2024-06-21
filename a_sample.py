'''
Author: Mr.Car
Date: 2024-06-21 15:06:42
'''
import os
from inner import JSBG_7
from alive_progress import alive_bar
from inner.share import *
from inner.load_config import ConfigLoader

config_loader = ConfigLoader()
yaml_data = config_loader.yaml
csv_data = config_loader.csv
inner_xls_template_path = config_loader.inner_xls_template_path
cfg_index = config_loader.cfg_index


def batch_type_7(file_pth, table_list, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = len(table_list) + 1
    with alive_bar(total_steps, title="7-53:表层样数据分析:") as bar:
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

def sample(file_pth, out_file_pth=None, xls_template_path=inner_xls_template_path):
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
    batch_type_7(file_pth, type_7_list, xls_template_path, out_file_pth)