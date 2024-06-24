import pandas as pd
import numpy as np
import re
from .share import fill_template, fill_title, get_sheet, XlsPosUtil, _get_devided_result
xpu = XlsPosUtil()

def _create_target_df(df, group_field_value):
    for each_col in group_field_value:
        if each_col not in df.columns:
            df = df.assign(**{each_col: 0})
    return df[group_field_value]

def _get_result_list(df, pivot_df, col_sum_names, col_sum_value, col_name_field, col_value_field, result_start_position):
    col_name_list = []
    result_list = []
    
    unique_df = df.drop_duplicates(subset = col_value_field, keep='first')
    unique_df = unique_df.sort_values(by = col_value_field, ascending=True)
    col_tuple_list = zip(unique_df[col_value_field], unique_df[col_name_field])

    for i, each_rule in enumerate(col_sum_value):
        col_name_list.append(col_sum_names[i]) # 整理 col_sum_name 到 name_list
        temp_df = pivot_df.query(f"{col_value_field}.str.match({each_rule})")
        sum_result = pivot_df.query(f"{col_value_field}.str.match({each_rule})").sum().tolist()
        result_list.append(sum_result) # 整理 sum_result 到 result

        small_values_list = [(value, name) for value, name in col_tuple_list if re.match(each_rule[1:-1], value)]
        for each_value, each_name in small_values_list:
            col_name_list.append(each_name)
            result = pivot_df[pivot_df.index == each_value].iloc[0].to_list()
            result_list.append(result)
    col_name_list.append('合计')
    result_list.append(np.array(result_list).sum(axis=0).tolist())
    [each.append(sum(each)) for each in result_list]
    result_list = list(map(list, zip(*result_list))) # 转置
    result_start_position_list = [xpu.position_add_col(result_start_position, i) for i in range(len(result_list))]
    return col_name_list, result_start_position_list, result_list


def statistics_all(df, yaml_data, wb, bar):
    '''
    计算表63: 各土类适宜等级面积分布表
    '''
    sheet_name = "SUITI_71"
    title = yaml_data[sheet_name]["title"]
    col_sum_names = yaml_data[sheet_name]["col_sum_names"]
    col_sum_value = yaml_data[sheet_name]["col_sum_value"]
    col_name_field = yaml_data[sheet_name]["col_name_field"]
    col_value_field = yaml_data[sheet_name]["col_value_field"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    group_field = yaml_data[sheet_name]["group_field"]
    group_field_value = map(str, yaml_data[sheet_name]["group_field_value"])
    col_start_position = yaml_data[sheet_name]["col_start_position"]
    result_start_position = yaml_data[sheet_name]["result_start_position"]

    df.loc[:, group_field + '_new'] = df[group_field].astype(str)
    '''
    s_level          3
    DLBM              
    0101     96.806396
    0103     20.146711
    0201     15.131976
    0202     14.683231
    0204     88.405779
    '''
    pivot_df = pd.pivot_table(df, values=calc_field, index=[col_value_field], columns=[group_field + '_new'], aggfunc='sum')
    pivot_df = _create_target_df(pivot_df, list(group_field_value))
    col_name_list, result_start_position_list, result_list = _get_result_list(df, pivot_df, col_sum_names, col_sum_value, col_name_field, col_value_field, result_start_position)

    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, col_start_position, col_name_list, False)
    for index, each in enumerate(result_start_position_list):
        fill_template(sheet, each, map(str, result_list[index]), False)
    bar()
    return wb