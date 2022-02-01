import os
import subprocess
import sys

from os import PathLike
from pathlib import Path
from typing import Any, Mapping, Optional

from pyhocon import ConfigFactory
from pyhocon.config_tree import ConfigTree
from pyhocon.converter import HOCONConverter

from koapy.utils.platform import is_32bit, is_64bit

# Type alias for config object
Config = ConfigTree


# Paths related to default config file
# bundled with this package for fallback
default_config_filename = "config.conf"
default_config_file_directory = os.path.dirname(os.path.realpath(__file__))
default_config_filepath = os.path.join(
    default_config_file_directory, default_config_filename
)


# Paths related to user config file
# for use customization
current_working_directory = os.getcwd()
home_directory = os.path.expanduser("~")

default_user_config_filename = "koapy.conf"

user_config_filename_cadidates = [
    default_user_config_filename,
    "." + default_user_config_filename,
]

default_user_config_filepath = os.path.join(
    home_directory,
    default_user_config_filename,
)


# Default encoding for all file read/writes across this package
default_encoding = "utf-8"


# Function for reading configs
def read_config(
    filename: Optional[PathLike] = None,
    encoding: Optional[str] = None,
) -> Config:
    if filename is None:
        filename = default_user_config_filepath
    if encoding is None:
        encoding = default_encoding
    # pylint: disable=redefined-outer-name
    config = ConfigFactory.parse_file(filename, encoding=encoding)
    return config


# Function for create configs from dict
def config_from_dict(dictionary: Mapping[str, Any]) -> Config:
    # pylint: disable=redefined-outer-name
    config = ConfigFactory.from_dict(dictionary)
    return config


# Load default config bundled with this package for fallback
default_config = read_config(default_config_filepath)


# Try to read user config file from candidate paths
#   1. Starting from current directory, search for a user config file until reaching the root directory, with specific name patterns
#   2. In terms of user config filename pattern, visible filename takes precedence to hidden filename (hidden that starts with a dot)
#   3. If fails to find a user config file even in the root directory, finally check user home directory for a user config file


# Search for a user config file in a given directory
def find_user_config_file_in(
    searching_directory: Optional[PathLike] = None,
) -> Optional[Path]:
    if searching_directory is None:
        # pylint: disable=redefined-outer-name
        current_working_directory = os.getcwd()
        searching_directory = current_working_directory
    searching_directory_path = Path(searching_directory).resolve()
    for config_filename in user_config_filename_cadidates:
        config_filepath = searching_directory_path / config_filename
        if config_filepath.exists():
            return config_filepath


# Search for a user config file from a given directory to the root directory
def find_user_config_file_from(
    starting_directory: Optional[PathLike] = None,
) -> Optional[Path]:
    if starting_directory is None:
        # pylint: disable=redefined-outer-name
        current_working_directory = os.getcwd()
        starting_directory = current_working_directory
    searching_directory_path = Path(starting_directory).resolve()
    should_stop = False
    while not should_stop:
        config_filepath = find_user_config_file_in(searching_directory_path)
        if config_filepath:
            return config_filepath
        has_no_more_parent = (
            str(searching_directory_path) == searching_directory_path.anchor
        )
        should_stop = has_no_more_parent
        searching_directory_path = searching_directory_path.parent


# Empty config for internal usage
empty_config = config_from_dict({})

# Prepare user config before reading actual user config file (which may not exist)
user_config = empty_config

# Main config object for general use
# User config takes precedence and fallbacks to default config for missing entries
config = user_config.with_fallback(default_config)


# Helper function for updating `user_config`, mostly for internal use
# This also consequently updates `config` global variable
def set_user_config(c: Config) -> Config:
    global user_config  # pylint: disable=global-statement
    global config  # pylint: disable=global-statement
    user_config = c
    config = user_config.with_fallback(default_config)
    return user_config


# Function for config initialization
def initialize_config_from_given_path(filename: Optional[PathLike] = None) -> bool:
    user_config_filepath: Optional[PathLike] = None
    initialized = False

    # Use given filepath if possible
    if not user_config_filepath:
        if filename:
            filepath = Path(filename).resolve()
            if filepath.exists():
                user_config_filepath = filepath

    if user_config_filepath:
        # pylint: disable=redefined-outer-name
        user_config = read_config(user_config_filepath)
        set_user_config(user_config)
        initialized = True

    return initialized


# Function for config initialization
def initialize_config_from_expected_paths() -> bool:
    user_config_filepath: Optional[PathLike] = None
    initialized = False

    # Try searching starting from current directory to root
    if not user_config_filepath:
        user_config_filepath = find_user_config_file_from(current_working_directory)

    # Try searching in home directory
    if not user_config_filepath:
        user_config_filepath = find_user_config_file_in(home_directory)

    # If user config file is found, read the config file
    # This overwrites previously declared emtpy `user_config` global variable
    if user_config_filepath:
        # pylint: disable=redefined-outer-name
        user_config = read_config(user_config_filepath)
        set_user_config(user_config)
        initialized = True

    return initialized


# Just run basic initializtion for the first time
initialize_config_from_expected_paths()


# Simple helper function for getting config
def get_config() -> Config:
    return config


# Simple helper function for getting user config
def get_user_config() -> Config:
    return user_config


# Flag value for additional logging for debugging purpose (mainly in development process)
debug = False


# Dump config object to string
def dump_config(
    config: Config,
    compact: bool = False,
    indent: int = 4,
) -> str:
    # pylint: disable=redefined-outer-name
    hocon = HOCONConverter.to_hocon(config, compact=compact, indent=indent)
    return hocon


# Save config to file
def save_config(
    filename: PathLike,
    config: Optional[Config] = None,
    compact: bool = False,
    indent: int = 4,
    encoding: Optional[str] = None,
):
    # pylint: disable=redefined-outer-name
    if config is None:
        config = get_config()
    if encoding is None:
        encoding = default_encoding
    hocon = dump_config(config, compact=compact, indent=indent)
    with open(filename, "w", encoding=encoding) as f:
        f.write(hocon)


# Save user config to file (without default fallbacks)
def save_user_config(
    filename: Optional[PathLike] = None,
    user_config: Optional[Config] = None,
    compact: bool = False,
    indent: int = 4,
    encoding: Optional[str] = None,
):
    # pylint: disable=redefined-outer-name
    if filename is None:
        filename = default_user_config_filepath
    if user_config is None:
        user_config = get_user_config()
    if encoding is None:
        encoding = default_encoding
    save_config(filename, user_config, compact, indent, encoding)


# Helper functions for getting python executables below
def get_executable_from_conda_envname(envname: str) -> str:
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


def get_executable_from_conda_envpath(envpath: str) -> str:
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


def get_executable_from_executable_config(executable_config: Config) -> Optional[str]:
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


def get_32bit_executable() -> Optional[str]:
    if is_32bit():
        return sys.executable
    executable_config = config.get("koapy.python.executable.32bit")
    return get_executable_from_executable_config(executable_config)


def get_64bit_executable() -> Optional[str]:
    if is_64bit():
        return sys.executable
    executable_config = config.get("koapy.python.executable.64bit")
    return get_executable_from_executable_config(executable_config)
