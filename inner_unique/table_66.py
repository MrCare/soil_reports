'''
Author: Mr.Car
Date: 2024-04-26 14:01:15
'''
import re
import numpy as np
import pandas as pd
from inner_unique import yaml_loader

cfg = yaml_loader.data["table_66"]
denominator = cfg["denominator"]
limit_fields = cfg["limit_fields"]
cal_fields = cfg["cal_fields"]
summary_horizon = cfg["summary_horizon"]
summary_vertical = cfg["summary_vertical"]
summary_position = cfg["summary_position"]

def excel_position_cal(start, length, direction="h"):
    '''
    计算一个excel单元格的最终位置
    '''
    pattern = r'^([A-Z]+)([1-9]\d*)$'
    match = re.match(pattern, start)
    if match:
        col = match.group(1)
        row = int(match.group(2))
        if direction == 'h':  # 横向
            final_col = chr(ord(col) + length)
            final_row = row
        else:  # 纵向
            final_col = col
            final_row = row + length
        return f"{final_col}{final_row}"
    else:
        return ""

def table_66(df):
    df[denominator["name"]] = df[denominator["name"]].astype(float)
    total_area = df[denominator["name"]].sum()
    # 用一个df承接数据用于计算summary， 用一个数组承接单元格数据用于计算summary
    row_length = len(limit_fields) * 2
    col_length = len(cal_fields)
    calc_df = np.empty((row_length, col_length))
    result_list = []
    for i, each_field in enumerate(limit_fields):
        # calc value
        # 构造query 字符串
        start_position = each_field["position"]
        filters = each_field["filter"]
        def limit_condition(row):
            result = True
            for each in filters:
                if row[each["name"]] not in each["value"]:
                    result = False
            return result

        filtered_df=df[df.apply(limit_condition, axis=1)]
        for j, field in enumerate(cal_fields):
            def final_limit(row):
                result = False
                if row[field["name"]] in field["value"]:
                    result = True
                return result
            final_fieltered_df = filtered_df[filtered_df.apply(final_limit, axis=1)]
            # calc value
            result_value = 0 if final_fieltered_df.empty else final_fieltered_df[denominator["name"]].sum()
            result_value_percentage = result_value / total_area
            result_value_format = "{:.2f}".format(result_value)
            result_value_percentage_format = "{:.2f}".format(result_value_percentage)
            # calc position
            result_value_position = excel_position_cal(start_position, j, 'h')
            result_value_percentage_position = excel_position_cal(result_value_position, 1, 'v')
            # fill_in_df
            calc_df[i*2, j] = result_value
            calc_df[i*2+1,j] = result_value_percentage
            # fill_in_list
            result_list.append({
                'value': result_value,
                'form': result_value_format,
                'position': result_value_position
            })
            result_list.append({
                'value': result_value_percentage,
                'form': result_value_percentage_format,
                'position': result_value_percentage_position
            })
    # calc summary horizon
    calc_df = pd.DataFrame(calc_df)
    row_sums = calc_df.sum(axis=1)
    calc_df['row_sums'] = row_sums
    # calc summary vertical
    col_sums = calc_df.sum()

    # insert to result_list
    for sum_i, row_value in enumerate(row_sums):
        result_value = row_value
        result_value_format = "{:.2f}".format(result_value)
        start = excel_position_cal(summary_position, col_length, 'h')
        position = excel_position_cal(start, sum_i,'v')
        result_list.append({
            'value': result_value,
            'form': result_value_format,
            'position': position
        })
    
    for sum_j, col_value in enumerate(col_sums):
        result_value = col_value
        result_value_format = "{:.2f}".format(result_value)
        start = excel_position_cal(summary_position, row_length, 'v')
        position = excel_position_cal(start, sum_j, 'h')
        result_list.append({
            'value': result_value,
            'form': result_value_format,
            'position': position
        })
    return result_list