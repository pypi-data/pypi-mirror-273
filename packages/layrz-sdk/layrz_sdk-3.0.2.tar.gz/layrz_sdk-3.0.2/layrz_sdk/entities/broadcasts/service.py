""" Service entity """


class OutboundService:
  """
  Outbound service definition
  ---
  Attributes
    - pk : Service ID
    - name : Service Name
  """

  def __init__(self, pk: int, name: str) -> None:
    self.pk = pk
    self.name = name

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'OutboundService(pk={self.pk}, name={self.name})'

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable

  def __str__(self) -> str:
    """ Readable property """
    return self._readable
