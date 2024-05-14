""" Chart alignment """
from enum import Enum


class ChartAlignment(Enum):
  """
  Chart Alignment
  """
  CENTER = 'center'
  LEFT = 'left'
  RIGHT = 'right'

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
