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

def add_dl(row, field, new_field_name, new_field_name_rule):
    '''
    增加大类字段
    '''
    for i, each in enumerate(new_field_name_rule):
        if re.match(each[1:-1], row[field]):
            return new_field_name[i]

def _get_result_list(pivot_df_first, pivot_df_second, columns_values, col_name_list):
    result_list = []
    percent_list = []
    for each_col_name in col_name_list:
        result = []
        percent = []
        if each_col_name[0] == 0:
            for each_value in columns_values:
                try:
                    area = pivot_df_first.loc[each_col_name[1], each_value]
                    area = area if area else 0
                    result.append(area)
                    percent.append(f"{(area / pivot_df_first.loc[each_col_name[1], 'All'] * 100):.2f}%")
                except Exception as e:
                    result.append(0)
                    percent.append(f"{0 * 100:.2f}%")
                    logging.error(f"SUITI_66: {e}", exc_info=True)
        elif each_col_name[0] == 1:
            for each_value in columns_values:
                try:
                    index_field = (each_col_name[1], each_col_name[2])
                    area = pivot_df_second.loc[index_field, each_value]
                    area = area if area else 0
                    result.append(area)
                    percent.append(f"{(area / pivot_df_second.loc[index_field, 'All'] * 100):.2f}%")
                except Exception as e:
                    result.append(0)
                    percent.append(f"{0 * 100:.2f}%")
                    logging.error(f"SUITI_66: {e}", exc_info=True)
        result_list.append(result)
        percent_list.append(percent)
        
    return np.transpose(result_list), np.transpose(percent_list)


def statistics_all(df, yaml_data, wb, bar):
    sheet_name = "SUITI_66"
    title = yaml_data[sheet_name]["title"]
    values = yaml_data[sheet_name]["values"]
    field = yaml_data[sheet_name]["field"]
    new_field = yaml_data[sheet_name]["new_field"]
    new_field_name = yaml_data[sheet_name]["new_field_name"]
    new_field_name_rule = yaml_data[sheet_name]['new_field_name_rule']
    index = yaml_data[sheet_name]['index']
    columns = yaml_data[sheet_name]['columns']
    columns_values = yaml_data[sheet_name]['columns_values']
    col_name_list = yaml_data[sheet_name]['col_name_list']
    result_start_position = yaml_data[sheet_name]['result_start_position']
    percent_start_position = yaml_data[sheet_name]['percent_start_position']

    df[new_field] = df.apply(lambda row : add_dl(row, field, new_field_name, new_field_name_rule), axis=1)
    sheet = get_sheet(wb, sheet_name)
    pivot_df_first = pd.pivot_table(df, values=values, index=index[0], columns=columns, aggfunc="sum", margins=True)
    pivot_df_first = _create_target_df(pivot_df_first, columns_values)
    pivot_df_second = pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc="sum", margins=True)
    pivot_df_second = _create_target_df(pivot_df_second, columns_values)
    result_list, percent_list = _get_result_list(pivot_df_first, pivot_df_second, columns_values, col_name_list)

    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    for i, each_result in enumerate(result_list):
        position = xpu.position_add_col(result_start_position, i)
        fill_template(sheet, position, each_result, False, 1)
    for i, each_percent in enumerate(percent_list):
        position = xpu.position_add_col(percent_start_position, i)
        fill_template(sheet, position, each_percent, False, 1)
    bar()
    return wb