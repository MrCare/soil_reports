'''
Author: Mr.Car
Date: 2024-06-21 17:01:42
'''
import os
import yaml
import pandas as pd

class ConfigLoader:
    _instance = None
    _loaded = False
    _yaml = None
    _csv = None
    _inner_xls_template_path = None
    _cfg_index = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._folder_path = os.path.join(os.path.dirname(__file__), 'config')

    @property
    def yaml(self):
        if not self._loaded:
            self._load_config()
        return self._yaml

    @property
    def csv(self):
        if not self._loaded:
            self._load_config()
        return self._csv
    
    @property
    def inner_xls_template_path(self):
        if not self._loaded:
            self._load_config()
        return self._inner_xls_template_path

    @property
    def cfg_index(self):
        if not self._loaded:
            self._load_config()
        return self._cfg_index

    def _load_config(self):
        self._loaded = True
        self._csv = {}
        self._inner_xls_template_path = os.path.join(self._folder_path, 'cfg_template.xlsx')
        for root, dirs, files in os.walk(self._folder_path):
            for filename in files:
                if filename.endswith('.yaml'):
                    with open(os.path.join(root, filename), 'r', encoding='utf-8') as f:
                        self._yaml = yaml.safe_load(f) or {}
                if filename.endswith('.csv'):
                    file_path = os.path.join(root, filename)
                    dataframe = pd.read_csv(file_path)
                    dataframe.set_index('name', inplace=True)
                    self._csv[os.path.splitext(filename)[0]] = dataframe
            self._cfg_index = self._csv['cfg_index']

    def reload_config(self):
        '''Method to reload configuration files'''
        self._loaded = False
        self._load_config()

# Usage
config_loader = ConfigLoader()
yaml_data = config_loader.yaml
csv_data = config_loader.csv
inner_xls_template_path = config_loader.inner_xls_template_path
cfg_index = config_loader.cfg_index