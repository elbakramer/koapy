import os
import logging.config

from pyhocon import ConfigFactory

def read_config(filename):
    return ConfigFactory.parse_file(filename)

config_filename_cadidates = [
    'koapy.conf',
    '.koapy.conf',
]

# Load default config
default_config_filename = 'config.conf'
file_directory = os.path.dirname(os.path.realpath(__file__))
default_config_filepath = os.path.join(file_directory, default_config_filename)
default_config = read_config(default_config_filepath)

# Prepare to load config in cwd and home
empty_config = ConfigFactory.from_dict({})
current_directory_config = empty_config

home = os.path.expanduser('~')
cwd = os.getcwd()

config_folder_candidates = [
    cwd,
    home,
]

# Try to load config in cwd and home
for config_folder in config_folder_candidates:
    for config_filename in config_filename_cadidates:
        config_path = os.path.join(config_folder, config_filename)
        if os.path.exists(config_path):
            current_directory_config = read_config(config_path)
            break

# Fallback to default config if not applicable
config = current_directory_config.with_fallback(default_config)

# Load logging config from config
logging_config = config.get('koapy.utils.logging.config')
load_logging_config = config.get('koapy.utils.logging.load_config')

if logging_config and load_logging_config:
    logging.config.dictConfig(logging_config)

# Set QT_API env if using qtpy, should be imported prior to using qtpy (currenty obsolete)
qt_api = config.get('koapy.qtpy.qt_api', 'pyside2')
os.environ['QT_API'] = qt_api
