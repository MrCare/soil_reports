'''
Author: Mr.Car
Date: 2024-06-18 12:25:30
'''
import re
from .share import fill_template, get_sheet, fill_title, _get_weight_result, XlsPosUtil
from .QUAL_76_78 import _get_street_list

xpu = XlsPosUtil()

def _get_result_list(df,street_value_list, limit_field, calc_field, weight_field, dl_field, dl_rule):
    cn_list, dl_list = [], []
    df.loc[:,(dl_field + '_str')] = df[dl_field].astype(str)
    df.loc[:,(limit_field + '_str')] = df[limit_field].astype(str)
    for each in street_value_list:
        calc_df = df[df[(limit_field + '_str')] == str(each)].copy()
        calc_dl_df = calc_df.query(f"{dl_field + '_str'}.str.match({dl_rule})").copy()
        cn_list.append(_get_weight_result(calc_df, calc_field, weight_field))
        dl_list.append(calc_dl_df[calc_field].sum())
    return cn_list, dl_list

def statistics_all(df, csv_data, yaml_data, wb, bar):
    '''
    计算表75各街道产能
    '''

    sheet_name = "QUAL_75"
    sheet = get_sheet(wb, sheet_name)
    title = yaml_data[sheet_name]["title"]
    limit_field = yaml_data[sheet_name]["limit_field"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    weight_field = yaml_data[sheet_name]["weight_field"]
    dl_field = yaml_data[sheet_name]["dl_field"]
    dl_rule = yaml_data[sheet_name]["dl_rule"]
    street_start_position = yaml_data[sheet_name]["street_start_position"]
    result_start_position = yaml_data[sheet_name]["result_start_position"]


    street_value_list, street_title_list = _get_street_list(csv_data)
    cn_list, dl_list = _get_result_list(df, street_value_list, limit_field, calc_field, weight_field, dl_field, dl_rule)
    fill_title(sheet, title)
    fill_template(sheet, street_start_position, street_title_list,False)
    fill_template(sheet, result_start_position, cn_list, False)
    fill_template(sheet, xpu.position_add_col(result_start_position,1), dl_list, False)
    bar()
    return wb