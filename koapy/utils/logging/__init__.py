import logging
import inspect

from koapy.utils.logging.Logging import Logging

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

def loglevel_to_verbosity(loglevel=logging.WARNING):
    verbosity = 3 - (loglevel + 9) // 10
    if verbosity < 0:
        verbosity = 0
    return verbosity

def set_loglevel(loglevel=logging.WARNING, logger=None):
    if logger is None:
        logger = 'koapy'
    return logging.getLogger(logger).setLevel(loglevel)

def set_verbosity(verbosity=0, logger=None):
    if logger is None:
        logger = 'koapy'
    loglevel = verbosity_to_loglevel(verbosity)
    set_loglevel(loglevel, logger)
    return loglevel

def get_module_name(offset=0):
    frame_infos = inspect.stack()
    frame = frame_infos[1 + offset]
    module = inspect.getmodule(frame[0])
    module_name = module.__name__
    return module_name

def get_logger(name=None):
    if name is None:
        module_name = get_module_name(1)
        name = module_name
    logger = logging.getLogger(name)
    return logger

def get_logger_for(class_or_instance):
    class_or_instance_type = type(class_or_instance)
    if isinstance(class_or_instance, object):
        class_or_instance = class_or_instance.__class__
    if isinstance(class_or_instance, type) and issubclass(class_or_instance, object):
        module_name = class_or_instance.__module__
        class_name = class_or_instance.__name__
        logger_name = module_name + '.' + class_name
    else:
        raise TypeError('Unexpected argument type %s' % class_or_instance_type)
    logger = logging.getLogger(logger_name)
    return logger

def initialize_logging():
    Logging.__initialize_if_necessary() # pylint: disable=protected-access
