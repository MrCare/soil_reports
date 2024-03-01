'''
Author: Mr.Car
Date: 2024-02-29 17:22:13
'''
import pandas as pd
from .share import fill_template

def get_classification_var(rule_table):
    '''
    根据计算类型，计算出结果
    '''
    not_none_rule_table = rule_table[rule_table.index != "none"]
    result = not_none_rule_table["alias"].tolist()
    return result

def get_iterrows_var(df, field, target_field, rule_table, calc_field, parent_field):
    not_none_rule_table = rule_table[rule_table.index != "none"]
    rule_strs = not_none_rule_table['value']
    result = []
    for each in rule_strs:
        df_result = df[df[field].apply(lambda x: eval(each, {"x": x}))] # 把 第一等级的 PH 筛选出来了
        df_result = df_result[df_result[parent_field] == calc_field] # 把 第一等级的 PH 属于“耕地” 筛选出来了
        result.append(df_result[target_field].sum())
    return result

def get_summary_var(result_table):
    df = pd.DataFrame(result_table)
    result = df.sum().tolist()
    return result

def get_var(df, field, target_field, rule_table, calc_field, parent_field, nan_filler):
    '''
    根据计算类型，计算出结果
    '''
    not_none_rule_table = rule_table[rule_table.index != "none"]
    result = []
    if calc_field == "classification":
        result = not_none_rule_table["alias"].tolist()
    elif clac_field != "summary":
        rule_strs = not_none_rule_table['value']
        for each in rule_strs:
            df_result = df[df[field].apply(lambda x: eval(each, {"x": x}))] # 把 第一等级的 PH 筛选出来了
            df_result = df_result[df_result[parent_field] == calc_field] # 把 第一等级的 PH 属于“耕地” 筛选出来了
            result.append(df_result["MJ"].sum())
    else:
        rule_strs = not_none_rule_table['value']
        for each in rule_strs:
            df_result = df[df[field].apply(lambda x: eval(each, {"x": x}))] # 把 第一等级的 PH 筛选出来了
            df_result = df_result[df_result[parent_field] in [calc_field]] # 把 第一等级的 PH 属于“耕地” 筛选出来了
    return result

def statistics_all(df, field, target_field, var_table, rule_table, sheet, nan_filler):
    wb = None
    result_table = []
    for name, row in var_table.iterrows():
        calc_field = name
        parent_field = row['parent_field']
        if calc_field == "classification":
            result_table.append(get_classification_var(rule_table))
        elif calc_field != "summary":
            result_table.append(get_iterrows_var(df, field, target_field, rule_table, calc_field, parent_field))
        else:
            result_table.append(get_summary_var(result_table[1:]))
    i = 0
    for name, row in var_table.iterrows():
        start_position = row["start_position"]
        fill_template(sheet, start_position, result_table[i])
        i += 1
    return

def prepare(df):
    '''
    数据预处理，增加 DLDLMC 字段, 将地类名称统成“耕园林草”
    '''
    def get_DLDLMC(dlbm):
        if '01' in dlbm:
            return '耕地'        
        elif '02' in dlbm:
            return '园地'
        elif '03' in dlbm:
            return '林地'
        elif '04' in dlbm:
            return '草地'
        else:
            return None
    # 添加新的列 DLDLMC
    df['DLDLMC'] = df['DLBM'].apply(get_DLDLMC)
    return df