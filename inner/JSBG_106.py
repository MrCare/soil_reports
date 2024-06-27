'''
Author: Mr.Car
Date: 2024-06-26 13:10:30
'''
import pandas as pd
import numpy as np
import re
from .share import fill_template, fill_title, get_sheet, XlsPosUtil, _get_devided_result
from .SUITI_71 import _create_target_df
from .exception import logging

xpu = XlsPosUtil()

def _get_result_list(df, values, fields, rule):
    result_list = []
    for each_field in fields:
        result = []
        calc_df = df[eval(rule, {'x':df[each_field]})][each_field]
        for each in values:
            if each == 'count':
                result.append(calc_df.count())
            elif each == 'min':
                result.append(calc_df.min())
            elif each == 'max':
                result.append(calc_df.max())
            elif each == 'mean':
                result.append(calc_df.mean())
            elif each == 'std':
                result.append(calc_df.std())
        result_list.append(result)
    return np.transpose(result_list)

def statistics_all(df, yaml_data, wb, bar):
    sheet_name = "JSBG_106"
    title = yaml_data[sheet_name]["title"]
    values = yaml_data[sheet_name]["values"]
    fields = yaml_data[sheet_name]["fields"]
    rule = yaml_data[sheet_name]["rule"]
    col_start_position = yaml_data[sheet_name]["col_start_position"]
    value_start_position = yaml_data[sheet_name]["value_start_position"]
    result_start_position = yaml_data[sheet_name]['result_start_position']

    result_list = _get_result_list(df, values, fields, rule)

    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, col_start_position, fields, False)
    fill_template(sheet, value_start_position, values)
    for i, each_result in enumerate(result_list):
        position = xpu.position_add_col(result_start_position, i)
        fill_template(sheet, position, each_result, False)
    bar()
    return wb