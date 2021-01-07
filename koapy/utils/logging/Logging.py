import logging
import logging.config

import threading

class Logging:

    __initialized = False
    __init_lock = threading.RLock()

    def __init__(self):
        self.__logger = None

    @classmethod
    def __initialize_if_necessary(cls):
        if not Logging.__initialized:
            with Logging.__init_lock:
                if not Logging.__initialized:
                    Logging.__initialize()

    @classmethod
    def __initialize(cls):
        from koapy.config import config

        logging_config = config.get('koapy.utils.logging.config')
        load_logging_config = config.get_bool('koapy.utils.logging.load_config', True)

        if logging_config and load_logging_config:
            logging.config.dictConfig(logging_config)

    @property
    def logger(self):
        if self.__logger is None:
            Logging.__initialize_if_necessary()
            self.__logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__name__)
        return self.__logger
