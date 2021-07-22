from .Logging import Logging


def get_logger(name=None):
    return Logging.get_logger(name)


def verbosity_to_loglevel(verbosity):
    return Logging.verbosity_to_loglevel(verbosity)


def loglevel_to_verbosity(loglevel):
    return Logging.loglevel_to_verbosity(loglevel)


def set_loglevel(loglevel):
    root_package_name = __name__.split(".", maxsplit=1)[0]
    logger = get_logger(root_package_name)
    logger.setLevel(loglevel)


def set_verbosity(verbosity):
    loglevel = verbosity_to_loglevel(verbosity)
    set_loglevel(loglevel)
