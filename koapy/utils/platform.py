import platform
import sys


def is_windows():
    return sys.platform == "win32"


def is_32bit():
    return platform.architecture()[0] == "32bit"


def is_64bit():
    return platform.architecture()[0] == "64bit"
