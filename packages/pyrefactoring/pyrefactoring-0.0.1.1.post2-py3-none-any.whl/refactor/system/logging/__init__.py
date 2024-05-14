import logging
from logging import *

# Import root logger.
root = logging.getLogger()

# Import log handlers.
from .stdout import add_stdout_handler, add_file_handler
