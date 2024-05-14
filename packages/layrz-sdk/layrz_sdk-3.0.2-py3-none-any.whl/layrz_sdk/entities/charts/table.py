""" Number chart """


class TableHeader:
  """ Table header chart configuration """

  def __init__(self, label: str, key: str) -> None:
    """ Constructor
    ---
    Arguments
      - label : Label of the header
      - key : Key of the header
    """
    self.label = label
    self.key = key


class TableRow:
  """ Table row chart configuration """

  def __init__(self, data: dict) -> None:
    """ Constructor
    ---
    Arguments
      - data : Data of the row
    """
    self.data = data


class TableChart:
  """
  Table chart configuration
  """

  def __init__(self, columns: list[TableHeader], rows: list[TableRow]) -> None:
    """
    Constructor
    ---
    Arguments
      - columns : List of columns
      - rows : List of rows
    """
    self.columns = columns
    self.rows = rows

  def render(self) -> dict:
    """
    Render chart to a graphic Library.
    """
    return {
      'library': 'FLUTTER',
      'chart': 'TABLE',
      'configuration': self._render_flutter(),
    }

  def _render_flutter(self) -> dict:
    """
    Converts the configuration of the chart to a Flutter native components.
    """
    return {
      'columns': [{
        'key': column.key,
        'label': column.label
      } for column in self.columns],
      'rows': [{
        'data': row.data
      } for row in self.rows],
    }
