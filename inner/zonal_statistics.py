'''
Author: Mr.Car
Date: 2024-03-01 16:43:50
'''
import geopandas as gpd
from rasterstats import zonal_stats
from alive_progress import alive_bar

def zs(vector_file, raster_file, new_field, output_file, stats_way='mean'):
    total_steps = 4
    with alive_bar(total_steps) as bar:
        # 打开矢量文件
        data = zonal_stats(vector_file,raster_file,stats=[stats_way])
        bar()
        
        df = gpd.read_file(vector_file)
        bar()

        # 添加统计量到矢量文件中
        df[new_field] = [each[stats_way] for each in data]
        bar()

        # 保存结果到新的矢量文件
        df.to_file(output_file)
        bar()