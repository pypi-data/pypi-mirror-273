""" Custom Field entitiy """


class CustomField:
  """
  Custom field definition
  ---
  Attributes
    - name : Name of the custom field
    - value : Value of the custom field
  """

  def __init__(self, name: str, value: str) -> None:
    """ Constructor """
    self.name = name
    self.value = value

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'CustomField(name={self.name}, value={self.value})'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
