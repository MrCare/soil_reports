'''
Author: Mr.Car
Date: 2024-06-26 13:10:30
'''
import pandas as pd
import numpy as np
import re
from .share import fill_template, fill_title, get_sheet, XlsPosUtil, _get_devided_result
from .exception import logging

xpu = XlsPosUtil()

def _get_soil_list(csv_data):
    soil_list = csv_data["cfg_113_var"][1:-1]
    soil_value_list = soil_list.index
    soil_title_list = soil_list['title']
    return soil_value_list, soil_title_list

def _get_result_list(df, soil_value_list, values, field, weight):
    result_mean_list, result_std_list = [], []
    for each_soil in soil_value_list:
        calc_df = df[df[field] == each_soil]
        mean_list, std_list = [], []
        for each_value in values:
            mean = np.average(calc_df[each_value], weights=calc_df[weight])
            std = (((calc_df[each_value] - mean) ** 2 * calc_df[weight]).sum() / calc_df[weight].sum()) ** 0.5
            mean_list.append(mean)
            std_list.append(std)
        result_mean_list.append(mean_list)
        result_std_list.append(std_list)

    return np.transpose(result_mean_list), np.transpose(result_std_list)

def statistics_all(df, csv_data, yaml_data, wb, bar, sheet_name = "JSBG_108"):
    title = yaml_data[sheet_name]["title"]
    field = yaml_data[sheet_name]["field"]
    weight = yaml_data[sheet_name]["weight"]
    values = yaml_data[sheet_name]["values"]
    col_start_position = yaml_data[sheet_name]["col_start_position"]
    value_start_position = yaml_data[sheet_name]["value_start_position"]
    result_start_position = yaml_data[sheet_name]['result_start_position']

    soil_value_list, soil_title_list = _get_soil_list(csv_data)
    result_mean_list, result_std_list = _get_result_list(df, soil_value_list, values, field, weight)
    mean_start_position, std_start_position = result_start_position, xpu.position_add_row(result_start_position,1)
    
    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, col_start_position, soil_title_list, False, 1)
    fill_template(sheet, value_start_position, values)
    for i, each_result in enumerate(result_mean_list):
        position = xpu.position_add_col(mean_start_position, i)
        fill_template(sheet, position, each_result, False, 1)
    for i, each_result in enumerate(result_std_list):
        position = xpu.position_add_col(std_start_position, i)
        fill_template(sheet, position, each_result, False, 1)
    bar()
    return wb