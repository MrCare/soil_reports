'''
Author: Mr.Car
Date: 2024-06-17 12:53:04
'''
from .share import fill_template, fill_title, get_sheet, XlsPosUtil

xpu = XlsPosUtil()

def _get_devided_result(divider, denominator):
    result = 0
    if denominator != 0:
        result = divider / denominator
    return result

def _get_result_list(df, start_position, street_value_list, group_field, group_field_value, calc_field, limit_field):
    df.loc[:, limit_field+'_new'] = df[limit_field].astype(str)
    df.loc[:, group_field+'_new'] = df[group_field].astype(str)
    area_list = []
    percent_list = []
    area_position_list = []
    percent_position_list = []

    area_sum_list = []
    percent_sum_list = []


    # 处理位置关系
    area_row, area_col = xpu.get_row_col(start_position)
    percent_row, percent_col = area_row + 1, area_col

    for i, each_field_level in enumerate(group_field_value):
        each_level_area_result = []
        each_level_percent_result = []
        grouped_df = df[df[group_field+'_new'] == str(each_field_level)].copy()
        for each_street in street_value_list:
            calc_df = grouped_df[grouped_df[limit_field + '_new'] == str(each_street)].copy()
            limited_df = df[df[limit_field + '_new'] == str(each_street)].copy()
            each_level_area_result.append(calc_df[calc_field].sum()) #  某街道某等级面积
            each_level_percent_result.append(_get_devided_result(calc_df[calc_field].sum(), limited_df[calc_field].sum()))
        total_area = sum(each_level_area_result)
        total_percent = total_area / df[calc_field].sum()
        each_level_area_result.append(total_area) # 先计算按行总计
        each_level_percent_result.append(total_percent)
        area_list.append(each_level_area_result)
        percent_list.append(each_level_percent_result)
        area_position_list.append(xpu.get_excel_position(area_row, area_col + i))
        percent_position_list.append(xpu.get_excel_position(percent_row, area_col + i))
    area_sum_list = [sum([each[i] for each in area_list]) for i in range(len(area_list[0]))] # 统一计算按列求和
    percent_sum_list = [sum([each[i] for each in percent_list]) for i in range(len(percent_list[0]))] # 统一计算按列求和
    area_list.append(area_sum_list) # 后计算按列总计
    percent_list.append(percent_sum_list)
    area_position_list.append(xpu.get_excel_position(area_row, area_col + len(group_field_value)))
    percent_position_list.append(xpu.get_excel_position(percent_row, area_col + len(group_field_value)))

    return area_position_list, area_list, percent_position_list, percent_list

def statistics_all(df, yaml_data, wb, bar, sheet_name="SUITI_64"):
    '''
    计算表63: 各土类适宜等级面积分布表
    '''
    title = yaml_data[sheet_name]["title"]
    limit_field = yaml_data[sheet_name]["limit_field"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    group_field = yaml_data[sheet_name]["group_field"]
    group_field_value = yaml_data[sheet_name]["group_field_value"]
    col_start_position = yaml_data[sheet_name]["col_start_position"]
    result_start_position = yaml_data[sheet_name]["result_start_position"]

    col_value_list = df[limit_field].unique().tolist()
    area_position_list, area_list, percent_list_position_list, percent_list = _get_result_list(df, result_start_position, col_value_list, group_field, group_field_value, calc_field, limit_field)
    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, col_start_position, col_value_list, False, 1)
    for index, each in enumerate(area_position_list):
        fill_template(sheet, each, map(str, area_list[index]), False, 1)
    for index, each in enumerate(percent_list_position_list):
        fill_template(sheet, each, map(str, percent_list[index]), False, 1)
    bar()
    return wb