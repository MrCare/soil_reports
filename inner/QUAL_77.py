'''
Author: Mr.Car
Date: 2024-03-04 15:23:53
'''
from .share import fill_template, get_sheet, fill_title

        # street_start_position = row["street_start_position"]
        # result_start_position = row["result_start_position"]
        # calc_field = row["calc_field"]
        # limit_field = row["limit_field"]
        # group_field = row["group_field"]
        # group_field_value = row["group_field_value"]

def _get_street_list(csv_data):
    street_list = csv_data["cfg_112_var"][1:-1]
    street_value_list = street_list.index
    street_title_list = street_list['title']
    return street_value_list, street_title_list

def _get_result_list(street_value_list, df, calc_field, limit_field, group_field, group_field_value, weight_field):
    result_list = []
    df.loc[:,(group_field + '_str')] = df[group_field].astype(str)
    df.loc[:,(limit_field + '_str')] = df[limit_field].astype(str)
    grouped_df = df[df[(group_field + '_str')] == str(group_field_value)].copy()
    for each in street_value_list:
        calc_df = grouped_df[grouped_df[(limit_field + '_str')] == str(each)].copy()
        calc_df.loc[:, '_temp'] = calc_df[calc_field] * calc_df[weight_field]

        denominator = calc_df[calc_field].sum()
        if denominator != 0:
            result = format(calc_df['_temp'].sum() / calc_df[calc_field].sum(), '.2f')
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
        calc_field = row["calc_field"]
        limit_field = row["limit_field"]
        group_field = row["group_field"]
        group_field_value = row["group_field_value"]
        title = row["title"]

        f1_f = row["f1_f"]
        f2_f = row["f2_f"]
        f3_f = row["f3_f"]
        f4_f = row["f4_f"]

        f1_f_st = row["f1_f_st"]
        f2_f_st = row["f2_f_st"]
        f3_f_st = row["f3_f_st"]
        f4_f_st = row["f4_f_st"]        

        field_list = [f1_f,f2_f,f3_f,f4_f]
        field_position_list = [f1_f_st, f2_f_st, f3_f_st, f4_f_st]

        fill_title(sheet, title)
        fill_template(sheet, street_start_position, street_title_list,False)
        
        for index, each in enumerate(field_list):
            result_list = _get_result_list(street_value_list, df, calc_field, limit_field, group_field, group_field_value, each)
            fill_template(sheet, field_position_list[index], result_list,False)
        bar()
    return wb