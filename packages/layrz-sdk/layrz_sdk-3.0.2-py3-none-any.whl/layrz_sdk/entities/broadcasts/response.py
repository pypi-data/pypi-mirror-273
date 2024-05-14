""" Broadcast Result Response data """


class BroadcastResponse:
  """
  Broadcast response data
  ---
  Attributes
    - json (dict|list): Parsed data
    - raw (str): Raw data
  """

  def __init__(self, json: dict | list, raw: str) -> None:
    self.json = json
    self.raw = raw

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'BroadcastResponse(json={self.json}, raw={self.raw})'

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable

  def __str__(self) -> str:
    """ Readable property """
    return self._readable
