'''
Author: Mr.Car
Date: 2024-03-04 15:23:53
'''
import pandas as pd
import geopandas as gpd
import os
from .share import fill_template, _get_sorted_list
from .TRSX_111 import statistics_all as statistics_all



def prepare(origin_file_pth, folder_path, cfg_name, parent_field, sort_field=None, encoding='UTF-8', ):
    '''
    数据预处理，根据 parent_field 与 field 生成 cfg 配置文件
    包含 classification 与 summary
    '''
    cfg_pth = os.path.join(folder_path, cfg_name + '.csv')
    gdf = gpd.read_file(origin_file_pth, encoding=encoding)
    df = pd.DataFrame({'name':['classification'], 'start_position':['B3'], 'parent_field':[''], 'title':[''], 'locate_position':[''], 'calc_summary':['']})
    name_list = _get_sorted_list(gdf, parent_field, sort_field)
    parent_list = [parent_field for _ in name_list]
    title_list = [each for each in name_list]
    calc_summary_list = ['c' for each in name_list]

    name_list.append('summary')
    parent_list.append('')
    title_list.append('总计')
    calc_summary_list.append('')
    start_position_list = [('B' + str(4 + i)) for i in range(len(name_list))]
    locate_position_list = [('A' + str(4 + i)) for i in range(len(name_list))]

    data_df = pd.DataFrame({
        'name': name_list,
        'start_position': start_position_list,
        'parent_field': parent_list,
        'title': title_list,
        'locate_position': locate_position_list,
        'calc_summary': calc_summary_list
    })

    df = pd.concat([df, data_df])
    df.to_csv( cfg_pth, index = False )