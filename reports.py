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

from alive_progress import alive_bar
from inner import zonal_statistics, check, TRSX_112
from inner.share import *
from inner.exception import *
from inner.load_config import folder_path, inner_xls_template_path
from a_sample import sample
from b_element import element
from c_qual import qual
from d_suiti import suiti

# 忽略 FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)

def prepare_cfg(origin_file_pth, cfg_name, parent_field, sort_field=None):
    '''
    准备“街道”与“土类”字段: 112 与 113 类型的配置文件
    '''
    with alive_bar(1, title="生成配置文件:") as bar:
        TRSX_112.prepare(origin_file_pth, folder_path, cfg_name, parent_field, sort_field)
        bar()
    return "Done!"

def quality_check(shp, shp_type="sample"):
    '''
    文件质量检查
    '''
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

# def add_DL(shp):
#     total_steps = 3
#     with alive_bar(total_steps,title="合并地类名称:") as bar:
#         new_csv = os.path.join(os.path.dirname(shp), 'new_csv.csv')
#         df = gpd.read_file(shp, encoding="utf-8")
#         bar()
#         df = add_field.add_field(df)
#         bar()
#         df.to_csv(new_csv, encoding="utf-8")
#         bar()
#     return "Done!"

@catch_file_not_found_error
@catch_key_error
@add_attention
def total(sample_pth, element_pth, suiti_pth, qual_pth, range='ALL', out_file_pth=None):
    '''
    --sample_pth : 样点数据路径
    --element_pth : 评价单元数据路径
    --qual_pth : 耕地质量评价结果数据路径
    --suiti_pth : 适宜性评价结果数据路径
    --range: ALL | SAMPLE | ELEMENT | QUAL | SUITI
    '''
    xls_template_path = os.path.join(os.path.dirname(sample_pth), 'reports_result.xlsx')

    if range == "SAMPLE":
        sample(sample_pth, xls_template_path, inner_xls_template_path)
    elif range == "ELEMENT":
        element(element_pth, xls_template_path, inner_xls_template_path)
    elif range == "QUAL":
        qual(qual_pth, xls_template_path, inner_xls_template_path)
    elif range == "SUITI":
        suiti(suiti_pth, xls_template_path, inner_xls_template_path)
    elif range == "ALL":
        sample(sample_pth, xls_template_path)
        element(element_pth, xls_template_path, xls_template_path)
        qual(qual_pth, xls_template_path, xls_template_path)
        suiti(suiti_pth, xls_template_path, xls_template_path)
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
    # 生成配置文件

    # prepare_cfg('./test_data/element/element_short.shp','cfg_112_var','XZQMC', 'XZQDM')
    # prepare_cfg('./test_data/element/element_short.shp','cfg_113_var','TL')

    # 质量检查

    # quality_check("./test_data/表层样点.shp", shp_type='sample')
    # quality_check('./test_data/评价单元.shp', shp_type='element')
    
    # 总体测试

    # total('test_data/sample/sample_short.shp', 'test_data/element/element_short.shp', './test_data/suiti_result/suiti_result_short.shp', './test_data/quality_result/quality_short.shp', 'ALL')
    # batch_type_76("test_data/quality_result/quality_short.shp")

    fire.Fire({
        "zs": zonal_statistics.zs,
        "total": total,
        "get_var_table": prepare_cfg,
        "quality_check": quality_check,
    })
