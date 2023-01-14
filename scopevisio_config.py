import configparser
from typing import MutableMapping


def get_scopevisio_config(config_filename: str) -> MutableMapping:
    config = configparser.ConfigParser()
    config.read(config_filename)
    return config['SCOPEVISIO']
