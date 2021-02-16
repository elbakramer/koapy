import os

from pyhocon import ConfigFactory

def read_config(filename):
    return ConfigFactory.parse_file(filename)

config_filename_cadidates = [
    'koapy.conf',
    '.koapy.conf',
]

# Load default config
default_config_filename = 'config.conf'
default_config_file_directory = os.path.dirname(os.path.realpath(__file__))
default_config_filepath = os.path.join(default_config_file_directory, default_config_filename)
default_config = read_config(default_config_filepath)

# Prepare to load config in cwd and home
empty_config = ConfigFactory.from_dict({})
user_config = empty_config

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
            user_config = read_config(config_path)
            break

# Fallback to default config if not applicable
config = user_config.with_fallback(default_config)
