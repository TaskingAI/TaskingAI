import yaml
import json
import os
from configparser import ConfigParser
from backend.tests.common.logger import logger


class MyConfigParser(ConfigParser):

    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, option_str):
        return option_str

    def get_sections(self):
        return self._sections


class ReadFileData:

    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def load_yaml(self, data_path, yaml_file_name):
        file_path = os.path.join(self.base_path, f'common/data/{data_path}', yaml_file_name)
        logger.info("load {} file......".format(file_path))
        with open(file_path, encoding='utf-8') as f:
            _data = yaml.safe_load(f)
        logger.info("read data ==>>  {} ".format(_data))
        return _data

    def load_json(self):
        file_path = os.path.join(self.base_path, "config", "setting.json")
        logger.info("load {} file......".format(file_path))
        with open(file_path, encoding='utf-8') as f:
            _data = json.load(f)
        logger.info("read data ==>>  {} ".format(_data))
        return _data

    def load_ini(self):
        file_path = os.path.join(self.base_path, "config", "setting.ini")
        logger.info("load {} file......".format(file_path))
        config = MyConfigParser()
        config.read(file_path, encoding="UTF-8")
        _data = config.get_sections()
        return _data

    def write_yml(self, yaml_file_name, _data):
        file_path = os.path.join(self.base_path, "data", yaml_file_name)
        logger.info("load {} file......".format(file_path))
        with open(file_path,  'wb') as f:
            logger.info("write data ==>>  {} ".format(_data))
            yaml.safe_dump(_data, f, default_flow_style=False,
                           explicit_start=True, allow_unicode=True, encoding='utf-8')


data = ReadFileData()
