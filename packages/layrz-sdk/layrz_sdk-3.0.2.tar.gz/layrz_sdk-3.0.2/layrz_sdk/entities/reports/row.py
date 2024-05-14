""" Report row """

from .col import ReportCol


class ReportRow:
  """
  Report row definition

  Available attributes
  --------------------
    content (list(ReportCol)): Cols to display
    height (float): Height of the cell, in points (pt)
    compact (bool): Compact mode
  """

  def __init__(
    self,
    content: list[ReportCol],
    height: float = None,
    compact: bool = False,
  ) -> None:
    """ Constructor """
    self.content = content

    if height is not None:
      raise DeprecationWarning('height is deprecated, use height instead')

    self.compact = compact

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'ReportRow(content={self.content})'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
