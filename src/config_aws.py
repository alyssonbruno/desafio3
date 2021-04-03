"""
Configure aws
"""
from os import environ
from pytomlpp import load
from pathlib import Path
from botocore.config import Config


AWS_DIR_PATH = Path('/root/.aws')

class ConfigExecption(Exception):
    pass

class TomlConfig:
    def __init__(self, file_name):
        file_path = Path(file_name) if Path(file_name).exists() else Path(f'/etc/datachallenge/{file_name}')
        self.data = load(open(file_path))

    def __getattr__(self, item):
        if item in self.data:
            return self.data[item]

class S3Config:

    def __init__(self):
        self.user = None
        self.key = None
        self.region = None
        self.bucket_name = None
        self.make_config()

    def __load_config_from_toml(self):
        conf_file = TomlConfig('aws.toml')
        try:
            self.user = conf_file.aws['user']
            self.region = conf_file.aws['region']
            self.bucket_name = conf_file.aws['s3']['bucket']
            self.key = environ['AWS_S3_KEY']
        except KeyError:
            raise ConfigExecption('AWS configuration Error')

    def make_config(self) -> bool:
        self.__load_config_from_toml()
