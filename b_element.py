'''
Author: Mr.Car
Date: 2024-06-21 15:10:42
'''
import os
from inner import JSBG_8, TRSX_111, JSBG_108, JSBG_1
from alive_progress import alive_bar
from inner.share import *
from inner.load_config import ConfigLoader

config_loader = ConfigLoader()
yaml_data = config_loader.yaml
csv_data = config_loader.csv
inner_xls_template_path = config_loader.inner_xls_template_path
cfg_index = config_loader.cfg_index

def batch_type_111(file_pth, table_list, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = len(table_list) + 1
    with alive_bar(total_steps, title="8-54:评价单元数据分析:") as bar:
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

def batch_type_8(file_pth, table_list, xls_template_path=inner_xls_template_path, out_file_pth=None):
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

def type_108(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    sheet_name_list = ['JSBG_108', 'JSBG_109']
    total_steps = len(sheet_name_list) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="108-109:理化性质及肥力特征统计表:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        for sheet_name in sheet_name_list:
            wb = JSBG_108.statistics_all(df, csv_data, yaml_data, wb, bar, sheet_name)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_1(file_pth, xls_template_path=inner_xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="1:土壤类型面积统计表:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = JSBG_1.statistics_all(df, yaml_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def element(file_pth, out_file_pth=None, xls_template_path=inner_xls_template_path, ):
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

    batch_type_8(file_pth, type_8_list, xls_template_path, out_file_pth)
    batch_type_111(file_pth, type_111_list, out_file_pth, out_file_pth)
    type_108(file_pth, out_file_pth, out_file_pth)
    type_1(file_pth, out_file_pth, out_file_pth)

if __name__ == "__main__":
    type_1('/Users/car/Project/soilCli/reports/test_data/element/element_short.shp')