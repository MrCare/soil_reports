'''
Author: Mr.Car
Date: 2024-06-28 10:05:01
'''
import geopandas as gpd
from .SUITI_66 import add_dl
from .load_config import ConfigLoader

config_loader = ConfigLoader()
yaml_data = config_loader.yaml

def sample_joined(sample_df, element_df):
    sample_result = gpd.sjoin(sample_df, element_df, how='inner', op='within')
    return sample_result

def add_dldlmc(df):
    '''
    "field" : "DLBM"
    "new_field" : "DLDLMC"
    "new_field_name" : ["耕地", "园地", "林地", "草地", "其他"]
    "new_field_name_rule" : ["'^01'", "'^02'", "'^03'", "'^04'", "'^(?!(01|02|03|04))'"]    
    '''
    sheet_name = "SUITI_66"
    values = yaml_data[sheet_name]["values"]
    field = yaml_data[sheet_name]["field"]
    new_field = yaml_data[sheet_name]["new_field"]
    new_field_name = yaml_data[sheet_name]["new_field_name"]
    new_field_name_rule = yaml_data[sheet_name]['new_field_name_rule']

    df[new_field] = df.apply(lambda row : add_dl(row, field, new_field_name, new_field_name_rule), axis=1)
    return df
