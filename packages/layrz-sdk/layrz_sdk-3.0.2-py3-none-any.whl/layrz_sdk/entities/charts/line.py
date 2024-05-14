""" Line chart """

from .alignment import ChartAlignment
from .data_type import ChartDataType
from .exceptions import ChartException
from .serie import ChartDataSerie
from .serie_type import ChartDataSerieType


class LineChart:
  """
  Line chart configuration

  """

  def __init__(
    self,
    x_axis: ChartDataSerie,
    y_axis: list[ChartDataSerie],
    title: str = 'Chart',
    align: ChartAlignment = ChartAlignment.CENTER,
  ) -> None:
    """
    Constructor
    ----
    Arguments
      - x_axis : Defines the X Axis of the chart, uses the ChartDataSerie class.
                 Please read the documentation to more information.
      - y_axis : Defines the Y Axis of the chart, uses the ChartDataSerie class.
                 Please read the documentation to more information.
      - title : Title of the chart
      - align : Alignment of the title
    """
    for i, serie in enumerate(y_axis):
      if not isinstance(serie, ChartDataSerie):
        raise ChartException(f'Y Axis serie {i} must be an instance of ChartDataSerie')
    self.y_axis = y_axis

    if not isinstance(x_axis, ChartDataSerie):
      raise ChartException('X Axis must be an instance of ChartDataSerie')
    self.x_axis = x_axis

    if not isinstance(title, str):
      raise ChartException('title must be an instance of str')
    self.title = title

    if not isinstance(align, ChartAlignment):
      raise ChartException('align must be an instance of ChartAlignment')
    self.align = align

  def render(self, use_new_definition: bool = False) -> dict | list[dict]:
    """
    Render chart to a graphic Library.
    We have two graphic libraries: GRAPHIC and CANVASJS.

    GRAPHIC is a Flutter chart library. To return this option, use the parameter use_new_definition=True.
    CANVASJS is a Javascript chart library. This is the default option.
    """

    if use_new_definition:
      return {
        'library': 'GRAPHIC',
        'chart': 'LINE',
        'configuration': self._render_graphic(),
      }
    return {
      'library': 'CANVASJS',
      'chart': 'LINE',
      'configuration': self._render_canvasjs(),
    }

  def _render_graphic(self) -> list[dict]:
    """
    Converts the configuration of the chart to a Flutter library Graphic.
    """
    series = []

    for serie in self.y_axis:
      if serie.serie_type not in [ChartDataSerieType.LINE, ChartDataSerieType.AREA]:
        continue

      points = []

      for i, value in enumerate(self.x_axis.data):
        points.append({
          'x_axis': {
            'value': value.timestamp() if self.x_axis.data_type == ChartDataType.DATETIME else value,
            'is_datetime': self.x_axis.data_type == ChartDataType.DATETIME,
          },
          'y_axis': serie.data[i],
        })

      series.append({
        'group': serie.label,
        'color': serie.color,
        'dashed': serie.serie_type == ChartDataSerieType.LINE and serie.dashed,
        'type': 'AREA' if serie.serie_type == ChartDataSerieType.AREA else 'LINE',
        'values': points
      })

    return series

  def _render_canvasjs(self) -> dict:
    """
    Converts the configuration of the chart to Javascript library CanvasJS.
    """
    datasets = []

    for serie in self.y_axis:
      dataset = {
        'type': 'line',
        'name': serie.label,
        'connectNullData': True,
        'nullDataLineDashType': 'solid',
        'showInLegend': True,
        'color': serie.color,
        'markerSize': 3,
      }

      if serie.serie_type != ChartDataSerieType.NONE:
        dataset['type'] = serie.serie_type.value

      if serie.serie_type == ChartDataSerieType.AREA:
        dataset['fillOpacity'] = 0.3

      if self.x_axis.data_type == ChartDataType.DATETIME:
        dataset['xValueType'] = 'dateTime'
        dataset['xValueFormatString'] = 'YYYY-MM-DD HH:mm:ss TT'

      if serie.serie_type == ChartDataSerieType.LINE and serie.dashed:
        dataset['lineDashType'] = 'dash'
        dataset['markerSize'] = 0

      points = []

      if serie.serie_type == ChartDataSerieType.SCATTER:
        for point in serie.data:
          points.append({'x': point.x, 'y': point.y})
      else:
        for i, value in enumerate(self.x_axis.data):
          points.append({
            'x': (value.timestamp() * 1000) if self.x_axis.data_type == ChartDataType.DATETIME else value,
            'y': serie.data[i],
          })

      dataset['dataPoints'] = points
      datasets.append(dataset)

    return {
      'animationEnabled': False,
      'zoomEnabled': True,
      'title': {
        'text': self.title,
        'fontFamily': 'Fira Sans Condensed',
        'fontSize': 20,
        'horizontalAlign': self.align.value
      },
      'data': datasets,
      'axisX': {
        'title': self.x_axis.label,
        'titleFontFamily': 'Fira Sans Condensed',
        'titleFontSize': 20,
      },
      'toolTip': {
        'animationEnabled': False,
        'shared': True
      },
      'legend': {
        'cursor': 'pointer'
      }
    }


class AreaChart(LineChart):
  """
  Line chart
  
  Deprecation warning: This class will be removed in the next version. Use LineChart instead.
  """
