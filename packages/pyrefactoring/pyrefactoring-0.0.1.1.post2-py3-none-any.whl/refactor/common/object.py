from abc import ABC
from refactor.system import logging


class Object(ABC):
  """
  Base object includes useful utililities.
  """

  @property
  def logger(self) -> logging.Logger:
    """
    Get logger
    """
    return self.__logger
  
  def __init__(self, *args, **kwds):
    """
    Class constructor.
    :param args:  additional arguments.
    :param kwds:  additional keyword arguments.
    """
    self.__logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
  