import inspect

from koapy.utils.logging.Logging import Logging

get_logger = Logging.get_logger

verbosity_to_loglevel = Logging.verbosity_to_loglevel
loglevel_to_verbosity = Logging.loglevel_to_verbosity

set_loglevel = Logging.set_loglevel
set_verbosity = Logging.set_verbosity
