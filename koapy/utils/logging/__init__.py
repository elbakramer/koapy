import logging

def verbosity_to_loglevel(verbosity=0):
    verbosity = verbosity or 0
    levels = [
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]
    if verbosity >= len(levels):
        verbosity = -1
    level = levels[verbosity]
    return level

def set_loglevel(loglevel=logging.WARNING, logger=''):
    return logging.getLogger(logger).setLevel(loglevel)

def set_verbosity(verbosity=0):
    loglevel = verbosity_to_loglevel(verbosity)
    set_loglevel(loglevel)
    return loglevel
