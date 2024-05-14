""" Chart Serie type """
from enum import Enum


class ChartDataSerieType(Enum):
  """
  Chart data serie type
  """
  NONE = None
  LINE = 'line'
  AREA = 'area'
  SCATTER = 'scatter'

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
