'''
Author: Mr.Car
Date: 2024-04-25 16:56:05
'''
from inner_unique import yaml_loader

def _fullfill(row, superset):
    flag = False
    result_index = None
    for index, each in enumerate(superset):
        if each["include"] in str(row.loc[each["name"]]):
            flag = True
            result_index = index
            break
    return flag, index

def add_field(df):
    '''
    目的是将耕园林草大类统计出来:
    更抽象的功能：根据数据值的条件，添加相应字段
    '''
    df = df.drop('geometry', axis=1)
    cfg = yaml_loader.data["add_field"]
    for index, row in df.iterrows():
        flag, result_index = _fullfill(row, cfg["origin_fields"])
        if flag:
            for each in cfg["new_fields"][result_index]:
                df.at[index, each["name"]] = str(each["value"])
    return df