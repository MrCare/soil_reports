'''
Author: Mr.Car
Date: 2024-03-04 15:23:53
'''
import pandas as pd
import geopandas as gpd
import os
from .share import fill_template, get_sheet, fill_title
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message="Boolean Series key will be reindexed to match DataFrame index.")
# street_start_position = 'B2'
# result_start_position = 'B3'
# calc_field= 'MJ'
# group_field = 'dj'
# group_field_value = '1'
# table_name = 'QUAL_76'

def _get_street_list(csv_data):
    street_list = csv_data["cfg_112_var"][1:-1]
    street_value_list = street_list.index
    street_title_list = street_list['title']
    return street_value_list, street_title_list

def _get_result_list(street_value_list, df, calc_field, limit_field, group_field, group_field_value):
    result_list = []
    # TODO: 统一转化为 str 之后再进行比较
    grouped_df = df[df[group_field] == group_field_value]
    for each in street_value_list:
        calc_df = grouped_df[df[limit_field] == each]
        result = calc_df[calc_field].sum()
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
        limit_field = row["limit_field"]
        group_field = row["group_field"]
        group_field_value = row["group_field_value"]
        title = row["title"]

        result_list = _get_result_list(street_value_list, df, calc_field, limit_field, group_field, group_field_value)
        fill_title(sheet, title)
        fill_template(sheet, street_start_position, street_title_list, True)
        fill_template(sheet, result_start_position, result_list, True)
        bar()
    return wb