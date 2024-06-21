'''
Author: Mr.Car
Date: 2024-06-20 15:38:09
'''
from .share import fill_template, fill_title, get_sheet, XlsPosUtil

xpu = XlsPosUtil()

def _get_devided_result(divider, denominator):
    result = 0
    if denominator != 0:
        result = divider / denominator
    return result

def _get_col_list(df, col_name_field, col_value_field):
    temp_df = df[[col_name_field, col_value_field]].copy()
    unique_df = temp_df.drop_duplicates(subset = col_value_field, keep='first')
    unique_df = unique_df.sort_values(by = col_value_field, ascending=True)
    col_name_list = unique_df[col_name_field].tolist()
    col_value_list = unique_df[col_value_field].tolist()
    return col_name_list, col_value_list

def _get_result_list(df, start_position, col_name_field, col_value_field, col_sum_rule, col_sum_name, group_field, group_field_value, calc_field):
    df.loc[:, col_value_field+'_new'] = df[col_value_field].astype(str)
    df.loc[:, group_field+'_new'] = df[group_field].astype(str)
    area_list = []
    area_value_list = []
    percent_list = []
    area_position_list = []
    percent_position_list = []

    # 先搞定总计
    col_value_list = [col_sum_name]
    total_df = df.query(f"{col_value_field+'_new'}.str.match({col_sum_rule})").copy()
    for i, each_value in enumerate(group_field_value):
        calc_df = total_df[total_df[group_field+"_new"] == each_value].copy()
        result = calc_df[calc_field].sum()
        area_list.append([f"{result:.2f}"])
        area_value_list.append(result)
        area_position_list.append(xpu.position_add_col(start_position, i*2))
        percent_list.append(['100.00%'])
        percent_position_list.append(xpu.position_add_col(start_position, i*2+1))

    # 再分别统计
    special_col_name_list, special_col_value_list = _get_col_list(total_df, col_name_field, col_value_field)
    col_name_list = [col_sum_name] + special_col_name_list


    for i, each_value in enumerate(group_field_value):
        each_level_area_result = []
        each_level_percent_result = []
        grouped_df = total_df[total_df[group_field+'_new'] == str(each_value)].copy()
        for each_col_value in special_col_value_list:
            calc_df = grouped_df[grouped_df[col_value_field + '_new'] == str(each_col_value)].copy()
            area_list[i].append(calc_df[calc_field].sum())
            percent_list[i].append(_get_devided_result(calc_df[calc_field].sum(), area_value_list[i]))

    return area_position_list, area_list, percent_position_list, percent_list, col_name_list

def statistics_all(df, yaml_data, wb, bar, sheet_name="SUITI_67"):
    '''
    计算表63: 各土类适宜等级面积分布表
    '''
    title = yaml_data[sheet_name]["title"]
    col_name_field = yaml_data[sheet_name]["col_name_field"]
    col_value_field = yaml_data[sheet_name]["col_value_field"]
    col_sum_rule = yaml_data[sheet_name]["col_sum_rule"]
    col_sum_name = yaml_data[sheet_name]["col_sum_name"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    group_field = yaml_data[sheet_name]["group_field"]
    group_field_value = yaml_data[sheet_name]["group_field_value"]
    col_start_position = yaml_data[sheet_name]["col_start_position"]
    result_start_position = yaml_data[sheet_name]["result_start_position"]

    area_position_list,area_list,percent_list_position_list,percent_list,col_name_list = _get_result_list(df, result_start_position, col_name_field, col_value_field, col_sum_rule, col_sum_name, group_field, group_field_value, calc_field)

    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, col_start_position, col_name_list, False, 1)
    for index, each in enumerate(area_position_list):
        fill_template(sheet, each, map(str, area_list[index]), False, 1)
    for index, each in enumerate(percent_list_position_list):
        fill_template(sheet, each, map(str, percent_list[index]), False, 1)
    bar()
    return wb