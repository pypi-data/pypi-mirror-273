import os
import logging
from pathlib import Path
from datetime import datetime

# Define datetime format.
datefmt = "%d.%m.%Y-%H.%M.%S"
# Define logging format.
logfmt = "%(levelname)s pid(%(process)d) %(asctime)s.%(msecs)03d %(qualifiedFuncName)s() %(message)s"
logfmt = logging.Formatter(fmt=logfmt, datefmt=datefmt)


def logfilter(record) -> bool:
  """
  Filter log name and message.
  :param record:  log record.
  :return:        boolean.
  """
  if record.name == 'root':
    record.qualifiedFuncName = '.' + record.funcName
  else:
    record.qualifiedFuncName = record.name + '.' + record.funcName
  return True

def add_stdout_handler(
    logger = logging.getLogger(), 
    level: int = logging.DEBUG, 
    fmt: str = logfmt,
    filter = logfilter,
    *args, 
    **kwds
) -> logging.Logger:
  """
  Add standard output (console) log handler.
  :param logger:  logger to be added. Default is root logger.
  :param level:   log level to be handled.
  :param fmt:     log format string.
  :param args:    additional arguments.
  :param kwds:    additional keyword arguments.
  :return:        logger to be added.
  """
  handler = logging.StreamHandler()
  handler.setLevel(level)
  handler.setFormatter(fmt)
  handler.addFilter(filter)
  logger.addHandler(handler)
  return logger

def add_file_handler(
    logger = logging.getLogger(),
    level: int = logging.DEBUG,
    fmt: str = logfmt,
    filter = logfilter,
    dir: str = os.path.join(os.getcwd(), 'logs'),
    file: str = 'debug.txt',
    *args, 
    **kwds
) -> logging.Logger:
  """
  Add file log handler.
  :param logger:    logger to be added. Default is root logger.
  :param level:     log level to be handled.
  :param fmt:       log format string.
  :param filter:    log filter function.
  :param args:      additional arguments.
  :param kwds:      additional keyword arguments.
  :return:          logger to be added.
  """
  name, ext = os.path.splitext(file)
  name = f"{name}-{datetime.now().strftime(datefmt)}.{ext if len(ext) > 0 else 'txt'}"
  logfile = Path(dir)
  logfile.mkdir(parents=True, exist_ok=True)
  logfile = logfile.joinpath(name)
  handler = logging.FileHandler(str(logfile))
  handler.setLevel(level)
  handler.addFilter(filter)
  handler.setFormatter(fmt)
  logger.addHandler(handler)
