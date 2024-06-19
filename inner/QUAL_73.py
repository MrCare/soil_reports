'''
Author: Mr.Car
Date: 2024-06-17 12:53:04
'''
from .share import fill_template, fill_title, get_sheet, _get_weight_result
from .QUAL_76_78 import _get_street_list



def _get_score_list(df, street_value_list, calc_field, limit_field, weight_field):
    df.loc[:, limit_field+'_new'] = df[limit_field].astype(str)
    score_list = []
    for each_street in street_value_list:
        grouped_df = df[df[limit_field+'_new'] == str(each_street)].copy()
        result = _get_weight_result(grouped_df, calc_field, weight_field)
        score_list.append(result)
    # 获取县均值

    everage_score = _get_weight_result(df, calc_field, weight_field)
    score_list.append(everage_score)
    return score_list

def _get_level_list(score_list, level_table):
    level_list = []
    for each in score_list:
        result_level = [obj for obj in level_table if eval(obj["range"],{'x':float(each)})]
        level_list.append(result_level[0]["level_name"])
    return level_list

def statistics_all(df, csv_data, yaml_data, wb, bar):
    '''
    计算表73: 各乡镇（街道）耕地评价综合指数及质量等级表
    '''
    sheet_name = "QUAL_73"
    title = yaml_data[sheet_name]["title"]
    limit_field = yaml_data[sheet_name]["limit_field"]
    calc_field = yaml_data[sheet_name]["calc_field"]
    weight_field = yaml_data[sheet_name]["weight_field"]
    street_start_position = yaml_data[sheet_name]["street_start_position"]
    score_start_position = yaml_data[sheet_name]["score_start_position"]
    level_start_position = yaml_data[sheet_name]["level_start_position"]
    level_table = yaml_data[sheet_name]["level_table"]

    street_value_list, street_title_list = _get_street_list(csv_data)
    score_list = _get_score_list(df, street_value_list, calc_field, limit_field, weight_field)
    level_list = _get_level_list(score_list, level_table)
    sheet = get_sheet(wb, sheet_name)
    fill_title(sheet, title)
    fill_template(sheet, street_start_position, street_title_list, False)
    fill_template(sheet, score_start_position, score_list, False)
    fill_template(sheet, level_start_position, level_list, False)
    bar()
    return wb