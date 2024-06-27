'''
Author: Mr.Car
Date: 2024-06-25 16:04:14
'''
import pandas as pd
import numpy as np
import re
from .share import fill_template, fill_title, get_sheet, XlsPosUtil, _get_devided_result
from .QUAL_76_78 import _get_street_list

xpu = XlsPosUtil()

def _get_result_list(group_value_list, df, col_name_field, street_value_list,result_start_position,calc_field):
    result_position_list = []
    result_list = []

    for i, each_col_name in enumerate(group_value_list):
        pivot_df = pd.pivot_table(df, values=[calc_field], index=[col_name_field], columns=[each_col_name], aggfunc='sum', margins=True)
        last_col = pivot_df.columns[-1]  # 获取最后一列的列名
        pivot_df.drop(columns=[last_col], inplace=True)
        max_columns = pivot_df.idxmax(axis = 1)
        each_result_list = [max_columns[each_street][1] for each_street in street_value_list]
        each_result_list.append(max_columns["All"][1])
        result_list.append(each_result_list)
        result_position_list.append(xpu.position_add_col(result_start_position, i))
    return result_position_list, result_list


def statistics_all(df, csv_data, yaml_data, wb, bar):
    sheet_name = "SUITI_167"
    title = yaml_data[sheet_name]["title"]
    col_name_field = yaml_data[sheet_name]["col_name_field"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    group_value_list = yaml_data[sheet_name]["group_value_list"]
    group_start_position = yaml_data[sheet_name]["group_start_position"]
    col_start_position = yaml_data[sheet_name]["col_start_position"]
    result_start_position = yaml_data[sheet_name]["result_start_position"]
    
    sheet = get_sheet(wb, sheet_name)

    street_value_list, street_title_list = _get_street_list(csv_data)
    result_position_list, result_list = _get_result_list(group_value_list, df, col_name_field, street_value_list,result_start_position,calc_field)

    fill_title(sheet, title)
    fill_template(sheet, col_start_position, street_title_list, False)
    fill_template(sheet, group_start_position, group_value_list, True)
    for (i, each) in enumerate(result_position_list):
        fill_template(sheet, each, result_list[i], False)
    bar()
    return wb