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
        value_result = df_result[target_field].sum()
        result.append(value_result)
        # result.append( nan_filler if pd.isna(value_result) else str(round(value_result, 2)))
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
    result_calc_summary_table = []
    for name, row in var_table.iterrows():
        calc_field = name
        parent_field = row['parent_field']
        calc_summary = row['calc_summary']
        if calc_field == "classification":
            result_table.append(get_classification_var(rule_table))
        elif calc_field != "summary":
            result = get_iterrows_var(df, field, target_field, rule_table, calc_field, parent_field)
            result_table.append(result)
            if calc_summary == 'c':
                result_calc_summary_table.append(result)
        else:
            result_table.append(get_summary_var(result_calc_summary_table))

    # 格式化 result_table 
    formatted_table = []
    for row in result_table:
        formatted_row = []
        for item in row:
            if isinstance(item, (int, float)):
                formatted_row.append(f"{item:.2f}")
            else:
                formatted_row.append(item)
        formatted_table.append(formatted_row)
    
    # 填充数据
    i = 0
    for name, row in var_table.iterrows():
        start_position = row["start_position"]
        fill_template(sheet, start_position, formatted_table[i])
        i += 1
    return

def prepare(df):
    '''
    数据预处理，增加 DLDLMC 字段, 将地类名称统成“耕园林草”
    '''
    def get_DLDLMC(dlbm):
        dlbm_head = dlbm[:2]
        if dlbm_head == '01': # 01 开头 / 其他（）
            return '耕地'        
        elif dlbm_head == '02':
            return '园地'
        elif dlbm_head == '03':
            return '林地'
        elif dlbm_head == '04':
            return '草地'
        else:
            return '其他'
    # 添加新的列 DLDLMC
    df['DLDLMC'] = df['DLBM'].apply(get_DLDLMC)
    return df