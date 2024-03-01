'''
Author: Mr.Car
Date: 2024-01-07 23:07:27
'''
import pandas as pd
from .share import fill_template

def get_var(ss, rule_table, calc_type, nan_filler):
    '''
    根据计算类型，计算出结果
    '''
    not_none_rule_table = rule_table[rule_table.index != "none"]
    result = []
    if calc_type == "classification":
        result = not_none_rule_table["alias"].tolist()
    else:
        rule_strs = not_none_rule_table['value']
        df = pd.DataFrame()
        for each in rule_strs:
            s_result = ss[ss.apply(lambda x: eval(each, {"x": x}))]
            df = pd.concat([df, s_result], axis=1)
        if calc_type == "mean":
            raw_result = df.mean().tolist()
            result = [nan_filler if pd.isna(x) else f'{x:.2f}' for x in raw_result]
        elif calc_type == "count":
            raw_result = df.count().tolist()
            result = [str(x) for x in raw_result]
        elif calc_type == "percent":
            raw_result = df.count() / ss.count()
            result = [f'{x:.2f}' for x in raw_result.tolist()]
    return result

def statistics_all(ss, var_table, rule_table, sheet, nan_filler):
    wb = None
    for name, row in var_table.iterrows():
        calc_type = name
        start_position = row["start_position"]
        result_list = get_var(ss, rule_table, calc_type, nan_filler)
        fill_template(sheet, start_position, result_list)
    return