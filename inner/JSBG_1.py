'''
Author: Mr.Car
Date: 2024-06-26 13:10:30
'''
import pandas as pd
import numpy as np
import re
from .share import fill_template, fill_title, get_sheet, XlsPosUtil, _get_devided_result
from .SUITI_71 import _create_target_df
from .SUITI_66 import add_dl
from .exception import logging

xpu = XlsPosUtil()

def fill_none_nan_zero(value):
    return value if not (value is None or pd.isnull(value)) else 0

def _get_result_list(pivot_df, columns_values, col_name_list):
    result_list = []
    percent_list = []
    for each_col_name in col_name_list:
        result = []
        percent = []
        if each_col_name[0] == 0:
            for each_value in columns_values:
                try:
                    area = pivot_df_first.loc[each_col_name[1], each_value]
                    area = fill_none_nan_zero(area)
                    result.append(area)
                    percent.append(f"{fill_none_nan_zero(area / pivot_df_first.loc[each_col_name[1], 'All'] * 100):.2f}%")
                except Exception as e:
                    result.append(0)
                    percent.append(f"{0 * 100:.2f}%")
                    logging.error(f"SUITI_66: {e}", exc_info=True)
        elif each_col_name[0] == 1:
            for each_value in columns_values:
                try:
                    index_field = (each_col_name[1], each_col_name[2])
                    area = pivot_df_second.loc[index_field, each_value]
                    area = fill_none_nan_zero(area)
                    result.append(area)
                    percent.append(f"{fill_none_nan_zero(area / pivot_df_second.loc[index_field, 'All'] * 100):.2f}%")
                except Exception as e:
                    result.append(0)
                    percent.append(f"{0 * 100:.2f}%")
                    logging.error(f"SUITI_66: {e}", exc_info=True)
        result_list.append(result)
        percent_list.append(percent)
        
    return np.transpose(result_list), np.transpose(percent_list)


def statistics_all(df, yaml_data, wb, bar):
    sheet_name = "JSBG_001"
    title = yaml_data[sheet_name]["title"]
    values = yaml_data[sheet_name]["values"]
    field = yaml_data[sheet_name]["field"]
    new_field = yaml_data[sheet_name]["new_field"]
    new_field_name = yaml_data[sheet_name]["new_field_name"]
    new_field_name_rule = yaml_data[sheet_name]['new_field_name_rule']
    index = yaml_data[sheet_name]['index']
    columns = yaml_data[sheet_name]['columns']
    col_start_position = yaml_data[sheet_name]['col_start_position']
    row_start_position = yaml_data[sheet_name]['row_start_position']
    result_start_position = yaml_data[sheet_name]['result_start_position']

    df[new_field] = df.apply(lambda row : add_dl(row, field, new_field_name, new_field_name_rule), axis=1)
    sheet = get_sheet(wb, sheet_name)
    pivot_df = pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc="sum", margins=True)
    # pivot_df = _create_target_df(pivot_df, columns_values)
    # result_list = _get_result_list(pivot_df, columns_values, col_name_list)

    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, row_start_position, new_field_name)
    for i, each in enumerate(pivot_df.index):
        position = xpu.position_add_row(col_start_position, i)
        fill_template(sheet, position, each, True)
    for i, each in enumerate(new_field_name):
        position = xpu.position_add_col(result_start_position, i)
        fill_template(sheet, position, pivot_df[each], False)
    bar()
    return wb