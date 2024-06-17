'''
Author: Mr.Car
Date: 2024-06-17 12:53:04
'''
from .share import fill_template, fill_title, get_sheet
import openpyxl

def _get_excel_position(row, col):
    # openpyxl 没有直接提供转换函数，但可以使用 get_column_letter 函数
    # 来获取列的字母表示，然后拼接行号。
    col_letter = openpyxl.utils.get_column_letter(col)
    return f"{col_letter}{row}"

def _position_add_row(position, num):
    start_row, start_col = int(position[1:]), ord(position[0].upper()) - 64 # B4 转为 列标数字
    start_row += num
    return _get_excel_position(start_row, start_col)

def _position_add_col(position, num):
    start_row, start_col = int(position[1:]), ord(position[0].upper()) - 64 # B4 转为 列标数字
    start_col += num
    return _get_excel_position(start_row, start_col)


def segment(result_list, start_position, seg_length, position_interval, horizon=True):
    start_row, start_col = int(start_position[1:]), ord(start_position[0].upper()) - 64 # B4 转为 列标数字

    position_list = []
    group_result_list = []
    groups = len(result_list) // seg_length
    for i in range(groups):
        group_result_list.append(result_list[seg_length*i : seg_length*(i+1)])
        if horizon:
            start_row += i * position_interval
        else:
            start_col += i * position_interval
        position_list.append(_get_excel_position(start_row, start_col))
    return position_list, group_result_list
    

def statistics_all(df, yaml_data, wb, bar):
    '''
    计算表72: 耕地质量等级面积及其占比
    '''
    sheet_name = "QUAL_72"
    group_field = yaml_data[sheet_name]["group_field"]
    group_field_values = yaml_data[sheet_name]["group_field_values"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    title = yaml_data[sheet_name]["title"]
    start_position = yaml_data[sheet_name]["start_position"]
    seg_length = yaml_data[sheet_name]["seg_length"]
    position_interval = yaml_data[sheet_name]["position_interval"]

    denominator = df[calc_field].sum()
    area_result = []
    area_percent_result = []
    for group_field_value in group_field_values:
        grouped_df = df[df[group_field].astype(str) == str(group_field_value)].copy()
        area = grouped_df[calc_field].sum()
        area_percent = area / denominator
        area_result.append(format(area,'.2f'))
        area_percent_result.append(format(area_percent, '.2f'))
    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)

    position_list, group_result_list = segment(area_result,start_position, seg_length, position_interval, horizon=True)
    for index, each in enumerate(position_list):
        fill_template(sheet, each, group_result_list[index], True)
    bar()

    position_list, group_result_list = segment(area_percent_result,_position_add_row(start_position, 1), seg_length, position_interval, horizon=True)
    for index, each in enumerate(position_list):
        fill_template(sheet, each, group_result_list[index], True)
    return wb