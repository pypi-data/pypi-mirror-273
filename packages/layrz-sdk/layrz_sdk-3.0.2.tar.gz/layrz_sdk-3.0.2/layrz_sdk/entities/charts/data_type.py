""" Chart Data type """
from enum import Enum


class ChartDataType(Enum):
  """
  Chart Data Type
  """
  STRING = 'string'
  DATETIME = 'datetime'
  NUMBER = 'number'

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'BroadcastStatus.{self.value}'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
