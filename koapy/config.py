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

home = os.path.expanduser('~')
cwd = os.getcwd()

config_folder_candidates = [
    cwd,
    home,
]

for config_folder in config_folder_candidates:
    for config_filename in config_filename_cadidates:
        config_path = os.path.join(config_folder, config_filename)
        if os.path.exists(config_path):
            current_directory_config = read_config(config_path)
            break

config = current_directory_config.with_fallback(default_config)

logging_config = config.get('koapy.utils.logging.config')
load_logging_config = config.get('koapy.utils.logging.load_config')

if logging_config and load_logging_config:
    logging.config.dictConfig(logging_config)
