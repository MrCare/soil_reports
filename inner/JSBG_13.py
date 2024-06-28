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

def statistics_all(df, yaml_data, wb, bar, sheet_name = "JSBG_013"):
    title = yaml_data[sheet_name]["title"]
    values = yaml_data[sheet_name]["values"]
    index = yaml_data[sheet_name]['index']
    columns = yaml_data[sheet_name]['columns']
    col_start_position = yaml_data[sheet_name]['col_start_position']
    row_start_position = yaml_data[sheet_name]['row_start_position']
    result_start_position = yaml_data[sheet_name]['result_start_position']
    percent_start_position = yaml_data[sheet_name]['percent_start_position']

    sheet = get_sheet(wb, sheet_name)
    pivot_df = pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc="count",fill_value=0, margins=True)

    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, row_start_position, [each for each in pivot_df.columns])
    fill_template(sheet, col_start_position, [each for each in pivot_df.index], False, 1)
    for i, each in enumerate(pivot_df.columns):
        result_position = xpu.position_add_col(result_start_position, i)
        percent_position = xpu.position_add_col(percent_start_position, i)
        percent = (pivot_df[each] / pivot_df['All']).fillna(0).apply(lambda x: f"{x:.2f}%")
        fill_template(sheet, result_position, pivot_df[each], False, 1)
        fill_template(sheet, percent_position, percent, False, 1)
    bar()
    return wb