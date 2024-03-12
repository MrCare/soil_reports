'''
Author: Mr.Car
Date: 2024-03-08 15:08:02
'''
import pandas as pd

def prepare(df):
    return df

def calc(df, field, target_field):
    '''
    E(PH * mJ)
    '''
    result = (df[field] * df[target_field]).sum() / df[target_field].sum()
    return result

def format_value(val, nan_filler):
    if pd.isna(val) or val is None:
        return nan_filler
    elif isinstance(val, str):
        return val
    elif isinstance(val, (int, float)):
        return "{:.2f}".format(val)
    else:
        raise ValueError("Unsupported variable type")
    return

def fill_template(sheet, start_position, cluster_names, result_list, group_number, nan_filler):
    value_list = [format_value(val, nan_filler) for pair in zip(cluster_names, result_list) for val in pair]
    start_row, start_col = int(start_position[1:]), ord(start_position[0].upper()) - 64 # B4 转为 列标数字
    start_col_bak = start_col
    j = 0
    for each in value_list:
        sheet.cell(row=start_row, column=start_col, value=each)
        j += 1
        if j >= group_number:
            j = 0
            start_row += 1
            start_col = start_col_bak
        else:
            start_col += 1
    return sheet

def statistics_all(df, field, target_field, var_table, sheet, nan_filler):
    the_record = var_table.loc['table_eight']
    start_position = the_record['start_position'] # A2
    field # PH
    target_field # MJ
    parent_field = the_record['parent_field'] # XZQHBM
    group_number = the_record['group_number'] # 3
    # 街道列表
    unique_value_list = df[parent_field].unique().tolist()
    clustered_df = df.groupby(parent_field)
    cluster_names = list(clustered_df.groups.keys())
    result_list = clustered_df.apply(calc, field=field, target_field=target_field)
    fill_template(sheet, start_position, cluster_names, result_list, group_number, nan_filler)
    return df