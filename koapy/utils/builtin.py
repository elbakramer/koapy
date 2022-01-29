def dir_public(*args):
    return [name for name in dir(*args) if not name.startswith("_")]
