import platform


def is_32bit():
    return platform.architecture()[0] == "32bit"


def is_64bit():
    return platform.architecture()[0] == "64bit"
