import inspect
import logging
import logging.config
import threading


class LoggingMeta(type):

    __config = {
        "version": 1,
        "formatters": {
            "basic": {
                "format": "%(asctime)s [%(levelname)s] %(message)s - %(filename)s:%(lineno)d",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "NOTSET",
                "formatter": "basic",
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

    __initialized = False
    __init_lock = threading.RLock()

    def __initialize_if_necessary(cls):
        if not LoggingMeta.__initialized:
            with LoggingMeta.__init_lock:
                if not LoggingMeta.__initialized:
                    return LoggingMeta.__initialize(cls)

    def __initialize(cls):
        logging.config.dictConfig(LoggingMeta.__config)
        LoggingMeta.__initialized = True

    def __new__(cls, clsname, bases, dct):
        return super().__new__(cls, clsname, bases, dct)

    def __init__(cls, clsname, bases, dct):
        super().__init__(clsname, bases, dct)
        cls.__logger = None

    def __class_name(cls):
        class_name = cls.__name__
        if hasattr(cls, "__outer_class__"):
            class_name = "%s.%s" % (
                LoggingMeta.__class_name(cls.__outer_class__),
                class_name,
            )
        return class_name

    def __logger_name(cls):
        module = inspect.getmodule(cls)
        module_spec = module.__spec__
        if module_spec is not None:
            module_name = module_spec.name
        else:
            module_name = module.__name__
        class_name = LoggingMeta.__class_name(cls)
        logger_name = "%s.%s" % (module_name, class_name)
        return logger_name

    @property
    def logger(cls):
        if cls.__logger is None:
            LoggingMeta.__initialize_if_necessary(cls)
            logger_name = LoggingMeta.__logger_name(cls)
            cls.__logger = logging.getLogger(logger_name)
        return cls.__logger

    def get_logger(cls, name=None):
        if name is None:
            name = LoggingMeta.__logger_name(cls)
            if name == "__main__":
                name = "koapy"
        LoggingMeta.__initialize_if_necessary(cls)
        logger = logging.getLogger(name)
        return logger


class Logging(metaclass=LoggingMeta):
    @property
    def logger(self):
        return self.__class__.logger
