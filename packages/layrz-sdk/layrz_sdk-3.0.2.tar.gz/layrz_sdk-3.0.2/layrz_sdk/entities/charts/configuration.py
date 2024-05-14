""" Charts entities """


class ChartConfiguration:
  """
  Chart configuration
  """

  def __init__(self, name: str, description: str) -> None:
    """ Constructor """
    self.name = name
    self.description = description

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'ChartConfiguration(name="{self.name}")'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
