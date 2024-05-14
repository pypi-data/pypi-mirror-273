""" Number chart """


class NumberChart:
  """
  Number chart configuration
  """

  def __init__(self, value: int | float, color: str, label: str) -> None:
    """
    Constructor

    Arguments
    ---
    value : Value of the number
    color : Color of the number
    label : Label of the number
    """
    self.value = value
    self.color = color
    self.label = label

  def render(self) -> dict:
    """
    Render chart to a graphic Library.
    """
    return {
      'library': 'FLUTTER',
      'chart': 'NUMBER',
      'configuration': self._render_flutter(),
    }

  def _render_flutter(self) -> dict:
    """
    Converts the configuration of the chart to a Flutter native components.
    """
    return {
      'value': self.value,
      'color': self.color,
      'label': self.label,
    }
