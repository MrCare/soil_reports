'''
Author: Mr.Car
Date: 2024-03-04 15:23:53
'''
from .share import fill_template, get_sheet, fill_title

def _get_street_list(csv_data):
    street_list = csv_data["cfg_112_var"][1:-1]
    street_value_list = street_list.index
    street_title_list = street_list['title']
    return street_value_list, street_title_list

def _get_result_list(street_value_list, df, calc_field, weight_field, limit_field, group_field, group_field_value, table_type):
    result_list = []
    df.loc[:,(group_field + '_str')] = df[group_field].astype(str)
    df.loc[:,(limit_field + '_str')] = df[limit_field].astype(str)
    grouped_df = df.loc[df[(group_field + '_str')] == str(group_field_value)].copy()
    for each in street_value_list:
        calc_df = grouped_df.loc[grouped_df[(limit_field + '_str')] == str(each)].copy()
        if str(table_type) == "76":
            result = calc_df[calc_field].sum()
            result = f"{round(result, 2)}" if result != 0 else '/'
            result_list.append(result)
        elif str(table_type) == "78":
            denominator = calc_df[calc_field].sum()
            if denominator != 0:
                result = format((calc_df[calc_field] * calc_df[weight_field]).sum() / denominator, '.2f')
            else: 
                result = '/'
            result_list.append(result)
    return result_list

def statistics_all(df, var_table, csv_data, wb, bar):
    '''
    计算66与68类型的共计20张表数据，十等地分别统计产能与面积
    '''
    street_value_list, street_title_list = _get_street_list(csv_data)

    for name, row in var_table.iterrows():
        sheet_name = name
        sheet = get_sheet(wb, sheet_name)
        street_start_position = row["street_start_position"]
        result_start_position = row["result_start_position"]
        calc_field = row["calc_field"]
        weight_field = row["weight_field"]
        limit_field = row["limit_field"]
        group_field = row["group_field"]
        group_field_value = row["group_field_value"]
        table_type = row["table_type"]
        title = row["title"]
        result_list = _get_result_list(street_value_list, df, calc_field, weight_field, limit_field, group_field, group_field_value, table_type)
        fill_title(sheet, title)
        fill_template(sheet, street_start_position, street_title_list, True)
        fill_template(sheet, result_start_position, result_list, True)
        bar()
    return wb