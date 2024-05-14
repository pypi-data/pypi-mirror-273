""" Scatter chart """
from .alignment import ChartAlignment
from .exceptions import ChartException
from .serie_type import ChartDataSerieType


class ScatterSerieItem:
  """
  Chart Data Serie Item for Scatter Charts
  """

  def __init__(self, x: int | float, y: int | float) -> None:
    """
    Constructor

    Args
    ----
      x : X value of the item.
      y : Y value of the item.
    """
    self.x = x
    self.y = y


class ScatterSerie:
  """
  Chart Data Serie for Timeline charts
  """

  def __init__(
    self,
    data: list[ScatterSerieItem],
    color: str,
    label: str,
    serie_type: ChartDataSerieType = ChartDataSerieType.SCATTER,
  ) -> None:
    """
    Constructor
    ----
    Arguments
      data : List of data points.
      color : Color of the serie.
      label : Label of the serie.
    """
    for i, datum in enumerate(data):
      if not isinstance(datum, ScatterSerieItem):
        raise ChartException(f'Y Axis serie {i} must be an instance of ChartDataSerie')
    self.data = data

    if not isinstance(color, str):
      raise ChartException('color must be an instance of str')
    self.color = color

    if not isinstance(label, str):
      raise ChartException('label must be an instance of str')
    self.label = label

    if not isinstance(serie_type, ChartDataSerieType):
      raise ChartException('serie_type must be an instance of ChartDataSerieType')
    self.serie_type = serie_type


class ScatterChart:
  """
  Scatter chart configuration
  """

  def __init__(
    self,
    series: list[ScatterSerie],
    title: str = 'Chart',
    align: ChartAlignment = ChartAlignment.CENTER,
  ) -> None:
    """
    Constructor
    ----
    Arguments
      series : Defines the series of the chart, uses the ScatterSerie class.
               Please read the documentation to more information.
      title : Title of the chart.
      align : Alignment of the chart.
    """
    for i, serie in enumerate(series):
      if not isinstance(serie, ScatterSerie):
        raise ChartException(f'Y Axis serie {i} must be an instance of ScatterSerie')
    self.series = series

    if not isinstance(title, str):
      raise ChartException('title must be an instance of str')
    self.title = title

    if not isinstance(align, ChartAlignment):
      raise ChartException('align must be an instance of ChartAlignment')
    self.align = align

  def render(self, use_new_definition: bool = False) -> dict | list[dict]:
    """
    Render chart to a graphic Library.
    We have two graphic libraries: GRAPHIC and APEXCHARTS.

    GRAPHIC is a Flutter chart library. To return this option, use the parameter use_new_definition=True.
    APEXCHARTS is a Javascript chart library. This is the default option.
    """
    if use_new_definition:
      return {
        'library': 'GRAPHIC',
        'chart': 'SCATTER',
        'configuration': self._render_graphic(),
      }

    return {
      'library': 'APEXCHARTS',
      'chart': 'SCATTER',
      'configuration': self._render_apexcharts(),
    }

  def _render_graphic(self) -> list[dict]:
    """
    Converts the configuration of the chart to Flutter library Graphic.
    """
    series = []
    for serie in self.series:
      data = []

      type_serie = 'SCATTER'
      if serie.serie_type == ChartDataSerieType.SCATTER:
        type_serie = 'SCATTER'
      elif serie.serie_type == ChartDataSerieType.LINE:
        type_serie = 'LINE'
      elif serie.serie_type == ChartDataSerieType.AREA:
        type_serie = 'AREA'
      else:
        continue

      for item in serie.data:
        data.append({
          'x_axis': item.x,
          'y_axis': item.y,
        })

      series.append({
        'group': serie.label,
        'color': serie.color,
        'values': data,
        'type': type_serie,
      })

    return series

  def _render_apexcharts(self) -> dict:
    """
    Converts the configuration of the chart to Javascript library ApexCharts.
    """

    series = []
    colors = []

    for serie in self.series:
      data = []

      for item in serie.data:
        data.append([item.x, item.y])

      series.append({
        'name': serie.label,
        'data': data,
        'type': serie.serie_type.value,
      })
      colors.append(serie.color)

    config = {
      'series': series,
      'colors': colors,
      'title': {
        'text': self.title,
        'align': self.align.value,
        'style': {
          'fontFamily': 'Fira Sans Condensed',
          'fontSize': '20px',
          'fontWeight': 'normal'
        }
      },
      'chart': {
        'type': 'scatter',
        'animations': {
          'enabled': False
        },
        'toolbar': {
          'show': False
        },
        'zoom': {
          'enabled': False
        }
      },
      'dataLabels': {
        'enabled': True
      }
    }

    return config
