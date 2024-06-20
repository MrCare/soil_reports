'''
Author: Mr.Car
Date: 2024-06-17 12:53:04
'''
from .share import fill_template, fill_title, get_sheet, XlsPosUtil

xpu = XlsPosUtil()

def statistics_all(df, yaml_data, wb, bar, sheet_name="QUAL_72"):
    '''
    计算表72: 耕地质量等级面积及其占比
    '''
    group_field = yaml_data[sheet_name]["group_field"]
    group_field_values = yaml_data[sheet_name]["group_field_values"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    title = yaml_data[sheet_name]["title"]
    start_position = yaml_data[sheet_name]["start_position"]
    seg_length = yaml_data[sheet_name]["seg_length"]
    position_interval = yaml_data[sheet_name]["position_interval"]

    denominator = df[calc_field].sum()
    area_result = []
    _area_result_for_calc = []
    area_percent_result = []
    _area_percent_result_for_calc = []
    for group_field_value in group_field_values:
        grouped_df = df[df[group_field].astype(str) == str(group_field_value)].copy()
        area = grouped_df[calc_field].sum()
        area_percent = area / denominator
        area_result.append(f"{area:.2f}")
        _area_result_for_calc.append(area)
        area_percent_result.append(f"{(area_percent * 100):.2f}%")
        _area_percent_result_for_calc.append(area_percent)
    area_result.append(f"{sum(_area_result_for_calc):.2f}")
    area_percent_result.append(f"{sum(_area_percent_result_for_calc * 100):.2f}%")
    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)

    position_list, group_result_list = xpu.segment(area_result,start_position, seg_length, position_interval, horizon=True)
    for index, each in enumerate(position_list):
        fill_template(sheet, each, group_result_list[index], True)
    bar()

    position_list, group_result_list = xpu.segment(area_percent_result,xpu.position_add_row(start_position, 1), seg_length, position_interval, horizon=True)
    for index, each in enumerate(position_list):
        fill_template(sheet, each, group_result_list[index], True)
    return wb