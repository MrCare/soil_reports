'''
Author: Mr.Car
Date: 2024-01-18 20:39:58
Unique funciton for unique table
'''
import os
import yaml

class YamlLoader:
    def __init__(self, folder_path):
        self.data = {}
        self.load_yaml_files(folder_path)

    def load_yaml_files(self, folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.yaml'):
                    with open(os.path.join(root, file), 'r') as f:
                        data = yaml.load(f, Loader=yaml.FullLoader)
                        self.data.update(data)

# 使用示例
folder_path = os.path.join(os.path.dirname(__file__), 'config')
yaml_loader = YamlLoader(folder_path)