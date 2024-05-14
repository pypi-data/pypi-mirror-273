""" Broadcast Result Request data """


class BroadcastRequest:
  """
  Broadcast request data
  ---
  Attributes
    - json : Parsed data
    - raw : Raw data
  """

  def __init__(self, json: dict | list, raw: str) -> None:
    self.json = json
    self.raw = raw

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'BroadcastRequest(json={self.json}, raw={self.raw})'

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable

  def __str__(self) -> str:
    """ Readable property """
    return self._readable
