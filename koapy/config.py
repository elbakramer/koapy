import os
import logging.config

from pyhocon import ConfigFactory

def read_config(filename):
    return ConfigFactory.parse_file(filename)

config_filename_cadidates = [
    'koapy.conf',
    '.koapy.conf',
]

default_config_filename = 'config.conf'
file_directory = os.path.dirname(os.path.realpath(__file__))
default_config_filepath = os.path.join(file_directory, default_config_filename)
default_config = read_config(default_config_filepath)

empty_config = ConfigFactory.from_dict({})
current_directory_config = empty_config

cwd = os.getcwd()
for config_filename in config_filename_cadidates:
    config_path = os.path.join(cwd, config_filename)
    if os.path.exists(config_path):
        current_directory_config = read_config(config_path)
        break

config = current_directory_config.with_fallback(default_config)

logging.config.dictConfig(config.get('koapy.utils.logging'))
