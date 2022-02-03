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

    def get_logger(cls, name=None):
        LoggingMeta.__initialize_if_necessary(cls)
        logger = logging.getLogger(name)
        return logger

    def __module_name(cls):
        module = inspect.getmodule(cls)
        module_name = module.__spec__ and module.__spec__.name or module.__name__
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

    def get_class_logger(cls):
        name = LoggingMeta.__logger_name(cls)
        logger = LoggingMeta.get_logger(cls, name)
        return logger

    def get_module_logger(cls):
        name = LoggingMeta.__module_name(cls)
        logger = LoggingMeta.get_logger(cls, name)
        return logger

    def get_package_logger(cls):
        name = LoggingMeta.__module_name(cls)
        name = name.split(".", maxsplit=1)[0]
        logger = LoggingMeta.get_logger(cls, name)
        return logger

    def _logger(cls):
        if cls.__logger is None:
            cls.__logger = LoggingMeta.get_class_logger(cls)
        return cls.__logger

    @property
    def logger(cls):
        return LoggingMeta._logger(cls)

    def verbosity_to_loglevel(cls, verbosity):
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

    def loglevel_to_verbosity(cls, loglevel):
        verbosity = 3 - (loglevel + 9) // 10
        if verbosity < 0:
            verbosity = 0
        return verbosity

    def set_loglevel(cls, loglevel=logging.WARNING):
        return LoggingMeta._logger(cls).setLevel(loglevel)

    def set_verbosity(cls, verbosity=0):
        loglevel = LoggingMeta.verbosity_to_loglevel(cls, verbosity)
        LoggingMeta.set_loglevel(cls, loglevel)
        return loglevel

    def get_loglevel(cls):
        return LoggingMeta._logger(cls).level

    def get_verbosity(cls):
        loglevel = LoggingMeta.get_loglevel(cls)
        verbosity = LoggingMeta.loglevel_to_verbosity(cls, loglevel)
        return verbosity


class Logging(metaclass=LoggingMeta):
    @property
    def logger(self):
        return type(self)._logger()
