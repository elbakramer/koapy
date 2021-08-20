import os
import subprocess
import sys

from pyhocon import ConfigFactory
from pyhocon.converter import HOCONConverter

from koapy.utils.platform import is_32bit, is_64bit


# Read config function
def read_config(filename):
    return ConfigFactory.parse_file(filename)


# Create config from dict function
def config_from_dict(dictionary):
    return ConfigFactory.from_dict(dictionary)


# Load default config
default_config_filename = "config.conf"
default_config_file_directory = os.path.dirname(os.path.realpath(__file__))
default_config_filepath = os.path.join(
    default_config_file_directory, default_config_filename
)
default_config = read_config(default_config_filepath)

# Prepare to load config in cwd and home
empty_config = ConfigFactory.from_dict({})
user_config = empty_config

home = os.path.expanduser("~")
cwd = os.getcwd()

config_folder_candidates = [
    cwd,
    home,
]

config_filename_cadidates = [
    "koapy.conf",
    ".koapy.conf",
]

default_user_config_path = os.path.join(
    config_folder_candidates[0],
    config_filename_cadidates[0],
)

# Try to load config in cwd and home
for config_folder in config_folder_candidates:
    for config_filename in config_filename_cadidates:
        config_path = os.path.join(config_folder, config_filename)
        if os.path.exists(config_path):
            user_config = read_config(config_path)
            break

# Fallback to default config if not applicable
config = user_config.with_fallback(default_config)


# Flag value for additional logging for debug
debug = False


# Just to mitigate redefined outer name issue
global_config = config
global_user_config = user_config


# Save config functions
def dump_config(config, compact=False, indent=4):
    hocon = HOCONConverter.to_hocon(config, compact=compact, indent=indent)
    return hocon


def save_config(filename, config=None, compact=False, indent=4):
    if config is None:
        config = global_config
    hocon = dump_config(config, compact=compact, indent=indent)
    with open(filename, "w") as f:
        f.write(hocon)


def save_user_config(filename=None, user_config=None):
    if filename is None:
        filename = default_user_config_path
    if user_config is None:
        user_config = global_user_config
    save_config(filename, user_config)


# Helper functions below
def get_executable_from_conda_envname(envname):
    return subprocess.check_output(
        [
            "conda",
            "run",
            "-n",
            envname,
            "python",
            "-c",
            "import sys; print(sys.executable)",
        ],
        encoding=sys.stdout.encoding,
        creationflags=subprocess.CREATE_NO_WINDOW,
    ).strip()


def get_executable_from_conda_envpath(envpath):
    return subprocess.check_output(
        [
            "conda",
            "run",
            "-p",
            envpath,
            "python",
            "-c",
            "import sys; print(sys.executable)",
        ],
        encoding=sys.stdout.encoding,
        creationflags=subprocess.CREATE_NO_WINDOW,
    ).strip()


def get_executable_from_executable_config(executable_config):
    if isinstance(executable_config, str):
        return executable_config
    if isinstance(executable_config, dict):
        if "path" in executable_config:
            return executable_config["path"]
        if "conda" in executable_config:
            conda_config = executable_config["conda"]
            if isinstance(conda_config, str):
                envname = conda_config
                return get_executable_from_conda_envname(envname)
            if isinstance(conda_config, dict):
                if "name" in conda_config:
                    envname = conda_config["name"]
                    return get_executable_from_conda_envname(envname)
                if "path" in conda_config:
                    envpath = conda_config["path"]
                    return get_executable_from_conda_envpath(envpath)


def get_32bit_executable():
    if is_32bit():
        return sys.executable
    executable_config = config.get("koapy.python.executable.32bit")
    return get_executable_from_executable_config(executable_config)


def get_64bit_executable():
    if is_64bit():
        return sys.executable
    executable_config = config.get("koapy.python.executable.64bit")
    return get_executable_from_executable_config(executable_config)
