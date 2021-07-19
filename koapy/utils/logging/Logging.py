import inspect
import logging
import logging.config
import threading


class LoggingMeta(type):

    __default_config = {
        "version": 1,
        "formatters": {
            "default": {
                "format": "%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "NOTSET",
                "formatter": "default",
            },
        },
        "loggers": {
            "koapy": {
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        },
        "incremental": False,
        "disable_existing_loggers": False,
    }

    __config_key = "koapy.utils.logging.config"

    __initialized = False
    __init_lock = threading.RLock()

    def __initialize_if_necessary(cls):
        if not LoggingMeta.__initialized:
            with LoggingMeta.__init_lock:
                if not LoggingMeta.__initialized:
                    LoggingMeta.__initialize(cls)

    def __initialize(cls):
        from koapy.config import config

        logging_config_dict = config.get(
            LoggingMeta.__config_key, LoggingMeta.__default_config
        )

        logging.basicConfig()
        logging.config.dictConfig(logging_config_dict)
        LoggingMeta.__initialized = True

    def __new__(cls, clsname, bases, dct):
        return super().__new__(cls, clsname, bases, dct)

    def __init__(cls, clsname, bases, dct):
        super().__init__(clsname, bases, dct)
        cls.__logger = None

    def __get_name_from_module(cls, module):
        module_name = module.__name__
        module_spec = module.__spec__
        if module_spec is not None:
            module_name = module_spec.name
        return module_name

    def __module_name(cls):
        module = inspect.getmodule(cls)
        module_name = LoggingMeta.__get_name_from_module(cls, module)
        return module_name

    def __class_name(cls):
        class_name = cls.__name__
        if hasattr(cls, "__outer_class__"):
            class_name = "{}.{}".format(
                LoggingMeta.__class_name(cls.__outer_class__),
                class_name,
            )
        return class_name

    def __logger_name(cls):
        module_name = LoggingMeta.__module_name(cls)
        class_name = LoggingMeta.__class_name(cls)
        logger_name = "{}.{}".format(module_name, class_name)
        return logger_name

    def _get_logger(cls):
        if cls.__logger is None:
            LoggingMeta.__initialize_if_necessary(cls)
            logger_name = LoggingMeta.__logger_name(cls)
            cls.__logger = logging.getLogger(logger_name)
        return cls.__logger

    @property
    def logger(cls):
        return LoggingMeta._get_logger(cls)

    def get_logger(cls, name=None):
        if name is None:
            caller_frameinfo = inspect.stack()[1]
            caller_module = inspect.getmodule(caller_frameinfo.frame)
            name = LoggingMeta.__get_name_from_module(cls, caller_module)
        LoggingMeta.__initialize_if_necessary(cls)
        logger = logging.getLogger(name)
        return logger

    def verbosity_to_loglevel(cls, verbosity=0):
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

    def loglevel_to_verbosity(cls, loglevel=logging.WARNING):
        verbosity = 3 - (loglevel + 9) // 10
        if verbosity < 0:
            verbosity = 0
        return verbosity

    def set_loglevel(cls, loglevel=logging.WARNING, logger=None):
        if logger is None:
            logger = "koapy"
        return logging.getLogger(logger).setLevel(loglevel)

    def set_verbosity(cls, verbosity=0, logger=None):
        if logger is None:
            logger = "koapy"
        loglevel = LoggingMeta.verbosity_to_loglevel(cls, verbosity)
        LoggingMeta.set_loglevel(cls, loglevel, logger)
        return loglevel


class Logging(metaclass=LoggingMeta):
    @property
    def logger(self):
        return self.__class__._get_logger()
