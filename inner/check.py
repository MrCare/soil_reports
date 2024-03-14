import geopandas as gpd
import pandas as pd
import csv
from alive_progress import alive_bar

class FieldRule:
    def __init__(self, field, dtype, value_range=None, allow_empty=False):
        self.field = field
        self.dtype = dtype
        self.value_range = value_range
        self.allow_empty = allow_empty
    
    def validate(self, value):
        if self.dtype == 'int':
            if isinstance(value, int):
                if self.value_range:
                    return eval(self.value_range, {"x": value})
            else:
                return False
        elif self.dtype == 'float':
            if isinstance(value, float):
                if self.value_range:
                    return eval(self.value_range, {"x": value})
            else:
                return False
        elif self.dtype == 'str':
            if isinstance(value, str):
                if self.value_range:
                    return value in eval(self.value_range)
                else:
                    return True
            else:
                return False
        else:
            return False

    def get_description(self):
        description = f"字段'{self.field}'的值应该是{self.dtype}类型"
        if self.value_range:
            description += f"，且范围应该在{self.value_range}之间"
        if not self.allow_empty:
            description += "，且不能为空"
        return description

class FieldChecker:
    def __init__(self, global_rule_file):
        self.global_rules = self._read_rules(global_rule_file)
    
    def _read_rules(self, rule_file):
        rules = {}
        rules_df = pd.read_csv(rule_file)
        for _, row in rules_df.iterrows():
            field = row['name']
            dtype = row['type']
            value_range = row['range'] if row['range'] and not pd.isna(row['range']) else None
            allow_empty = row['isnull']
            rules[field] = FieldRule(field, dtype, value_range, allow_empty)
        return rules
    
    def _apply_rules(self, gdf, rules, bar):
        invalid_data = []
        for index, row in gdf.iterrows():
            for field, rule in rules.items():
                value = row.get(field, None)
                if not rule.validate(value):
                    invalid_data.append({
                        '文件名': gdf.at[index, 'filename'],
                        '行号': index + 1,
                        '字段名': field,
                        '不合格的值': value,
                        '不合格的原因': rule.get_description()
                    })
        bar()
        return invalid_data
    
    def check_file(self, shp_file, specific_rule_file=None):
        gdf = gpd.read_file(shp_file)
        gdf['filename'] = shp_file.split('/')[-1]
        
        rules = self.global_rules.copy()
        if specific_rule_file:
            specific_rules = self._read_rules(specific_rule_file)
            rules.update(specific_rules)
        
        with alive_bar(len(gdf)) as bar:
            invalid_data = self._apply_rules(gdf, rules, bar)
        
        return invalid_data

    def output_to_csv(self, data, output_file):
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = ['文件名', '行号', '字段名', '不合格的值', '不合格的原因']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in data:
                writer.writerow({
                    '文件名': entry['文件名'],
                    '行号': entry['行号'],
                    '字段名': entry['字段名'],
                    '不合格的值': entry['不合格的值'],
                    '不合格的原因': entry['不合格的原因'],
                })

def quality_check(global_rule_file, shp_files, output_file, specific_rule_files):
    '''
    数据质量检查
    '''
    checker = FieldChecker(global_rule_file)
    all_invalid_data = []
    for i, shp_file in enumerate(shp_files):
        if specific_rule_files:
            specific_rule_file = specific_rule_files[i]
            invalid_data = checker.check_file(shp_file, specific_rule_file)
        else:
            invalid_data = checker.check_file(shp_file)
        all_invalid_data.extend(invalid_data)
    if len(all_invalid_data) == 0:
        print("数据已经符合要求！")
    else:
        checker.output_to_csv(all_invalid_data, output_file)
        print(all_invalid_data)
        print(f"不合格数据已保存到 {output_file}。")