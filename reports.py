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

from inner import JSBG_7, JSBG_8, TRSX_111, TRSX_112, QUAL_76_78, QUAL_77, QUAL_72, zonal_statistics, check
from inner.share import fill_title, fill_value, get_sheet, ConfigLoader
# from inner_unique import add_field, table_66
from alive_progress import alive_bar
from openpyxl import load_workbook

# 忽略 FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

# 载入配置文件
folder_path = os.path.join(os.path.dirname(__file__), 'config')
xls_template_path = os.path.join(folder_path, 'cfg_template.xlsx')
configLoader = ConfigLoader(folder_path)# 载入配置文件
csv_data = configLoader.csv
yaml_data = configLoader.yaml
cfg_index = csv_data['cfg_index']

def read_and_prepare_file(file_pth, file_type="shp"):
    if file_type == 'csv':
        df = pd.read_csv(file_path)
    else:
        df = gpd.read_file(file_pth)
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

def batch_type_76(file_pth, xls_template_path=xls_template_path, out_file_pth=None):
    var_table = csv_data['cfg_76and78_var']
    total_steps = len(var_table) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="土壤质量等级面积与产能分布:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_76_78.statistics_all(df, var_table, csv_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def batch_type_77(file_pth, xls_template_path=xls_template_path, out_file_pth=None):
    var_table = csv_data['cfg_77_var']
    total_steps = len(var_table) + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="土壤质量属性情况:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_77.statistics_all(df, var_table, csv_data, wb, bar)
        save_xls(wb, out_file_pth)
        bar()
    return "Done!"

def type_72(file_pth, xls_template_path=xls_template_path, out_file_pth=None):
    total_steps = 1 + 1
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')
    with alive_bar(total_steps, title="土壤质量等级面积及其占比:") as bar:
        df = read_and_prepare_file(file_pth)
        wb = get_wb(xls_template_path)
        wb = QUAL_72.statistics_all(df, yaml_data, wb, bar)
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

def add_DL(shp):
    total_steps = 3
    with alive_bar(total_steps,title="合并地类名称:") as bar:
        new_csv = os.path.join(os.path.dirname(shp), 'new_csv.csv')
        df = gpd.read_file(shp, encoding="utf-8")
        bar()
        df = add_field.add_field(df)
        bar()
        df.to_csv(new_csv, encoding="utf-8")
        bar()
    return "Done!"

def _suiti_tables(file_pth, table_list, xls_template_path=xls_template_path, out_file_pth=None):
    df = read_and_prepare_file(file_pth)
    wb = get_wb(xls_template_path)
    if not out_file_pth:
        out_file_pth = os.path.join(os.path.dirname(file_pth), 'reports_result.xlsx')

    for table in table_list:
        _, _, _, _, title, nan_filler = get_cfg_params(cfg_index, table)
        sheet = get_sheet(wb, table)
        sheet = fill_title(sheet, title, "A1")
        if table == 'SUTI_66':
            result_list = table_66.table_66(df)
            for each in result_list:
                fill_value(sheet, each["form"], each["position"])
    save_xls(wb, out_file_pth)

def total(sample_pth, element_pth, suti_pth, qual_pth, type_list, out_file_pth=None):
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
    suti_list = [
        'SUTI_66'
        ]
    for each in type_list:
        if each == "JSBG_7":
            batch_type_7(sample_pth, type_7_list)
        elif each == "TRSX_111":
            # batch_type_111(element_pth, ['TRSX_111_PH', 'TRSX_135_OM', 'TRSX_114_CEC', 'TRSX_117_TRRZPJZ', 'TRSX_120_GZCHD', 'TRSX_123_TRZD', 'TRSX_126_TRSL', 'TRSX_129_TRFSL', 'TRSX_132_TRNL', 'TRSX_138_TN', 'TRSX_141_TP', 'TRSX_144_TK', 'TRSX_147_AP', 'TRSX_150_AK'], xls_template_path)
            batch_type_111(element_pth, type_111_list, xls_template_path, xls_template_path)
        elif each == "JSBG_8":
            batch_type_8(element_pth, type_8_list, xls_template_path, xls_template_path)
        elif each == "SUTI":
            _suiti_tables(suti_pth, suti_list, xls_template_path, xls_template_path)
        elif each == "QUAL_76_78":
            batch_type_76(qual_pth, xls_template_path, xls_template_path)
        elif each == "QUAL_77":
            batch_type_77(qual_pth, xls_template_path, xls_template_path)
        elif each == "QUAL_72":
            type_72(qual_pth, xls_template_path, xls_template_path)
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

    # prepare_cfg('./test_data/element/element_short.shp','cfg_112_var','XZQMC')
    # prepare_cfg('./test_data/element/element_short.shp','cfg_113_var','TL')

    # 批处理测试

    # batch_type_111('./test_data/PH_OM评价单元.shp', ['TRSX_112_PH', 'TRSX_113_PH'])
    # batch_type_8('./test_data/评价单元.shp', ['JSBG_8_PH'])

    # 质量检查

    # quality_check("./test_data/表层样点.shp", shp_type='sample')
    # quality_check('./test_data/评价单元.shp', shp_type='element')
    
    #总体测试
    # add_DL("./test_data/suiti_result/suiti_result.shp")
    # total('test_data/sample/sample_short.shp', 'test_data/element/element_short.shp', './test_data/suiti_result/new_csv.csv', './test_data/quality_result/quality_short.shp', [
    #     'JSBG_7',
    #     'JSBG_8',
    #     'TRSX_111',
    #     'QUAL_76_78'
    #     'QUAL_77',
    #     'QUAL_72'
    # ])
    # total('test_data/sample/sample_short.shp', 'test_data/element/element_short.shp', './test_data/suiti_result/new_csv.csv', './test_data/quality_result/quality_short.shp', [
    #     'QUAL_76_78'
    # ])

    # batch_type_76("test_data/quality_result/quality_short.shp")

    fire.Fire({
        "zs": zonal_statistics.zs,
        "total": total,
        "get_var_table": prepare_cfg,
        "quality_check": quality_check,
        "add_DL": add_DL,
    })
