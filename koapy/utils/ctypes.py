import ctypes


def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() != 0
