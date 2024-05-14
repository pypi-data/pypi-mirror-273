""" Column chart """
from layrz_sdk.helpers import convert_to_rgba

from .alignment import ChartAlignment
from .exceptions import ChartException
from .serie import ChartDataSerie
from .serie_type import ChartDataSerieType


class ColumnChart:
  """
  Column chart configuration

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
    We have two graphic libraries: GRAPHIC and APEXCHARTS.

    GRAPHIC is a Flutter chart library. To return this option, use the parameter use_new_definition=True.
    APEXCHARTS is a Javascript chart library. This is the default option.
    """
    if use_new_definition:
      return {
        'library': 'GRAPHIC',
        'chart': 'COLUMN',
        'configuration': self._render_graphic(),
      }

    return {
      'library': 'APEXCHARTS',
      'chart': 'COLUMN',
      'configuration': self._render_apexcharts(),
    }

  def _render_graphic(self) -> list[dict]:
    """
    Converts the configuration of the chart to Flutter library graphic.
    """

    series = []

    for serie in self.y_axis:
      for i, value in enumerate(serie.data):
        x_axis = self.x_axis.data[i]
        series.append({
          'label': serie.label,
          'color': serie.color,
          'category': x_axis,
          'value': value,
        })

    return series

  def _render_apexcharts(self) -> dict:
    """
    Converts the configuration of the chart to Javascript library ApexCharts.
    """

    series = []
    colors = []
    stroke = {'width': [], 'dashArray': []}
    markers = []

    for serie in self.y_axis:
      modified_serie = {
        'name': serie.label,
      }
      if serie.serie_type == ChartDataSerieType.SCATTER:
        modified_serie['data'] = [{'x': item.x, 'y': item.y} for item in serie.data]
        modified_serie['type'] = 'scatter'
        stroke['width'].append(0)
        markers.append(10)
      else:
        modified_serie['data'] = [{'x': self.x_axis.data[i], 'y': item} for i, item in enumerate(serie.data)]

        if serie.serie_type is not ChartDataSerieType.NONE:
          modified_serie['type'] = serie.serie_type.value
        else:
          modified_serie['type'] = 'column'

        if serie.dashed and serie.serie_type == ChartDataSerieType.LINE:
          stroke['dashArray'].append(5)
        else:
          stroke['dashArray'].append(0)

        stroke['width'].append(3)
        markers.append(0)

      series.append(modified_serie)

      if serie.serie_type == ChartDataSerieType.AREA:
        color = convert_to_rgba(serie.color)
        colors.append(f'rgba({color[0]}, {color[1]}, {color[2]}, 0.5)')
      else:
        colors.append(serie.color)

    config = {
      'series': series,
      'colors': colors,
      'xaxis': {
        'type': self.x_axis.data_type.value,
        'title': {
          'text': self.x_axis.label,
          'style': {
            'fontFamily': 'Fira Sans Condensed',
            'fontSize': '20px',
            'fontWeight': 'normal'
          }
        }
      },
      'dataLabels': {
        'enabled': False
      },
      'title': {
        'text': self.title,
        'align': self.align.value,
        'style': {
          'fontFamily': 'Fira Sans Condensed',
          'fontSize': '20px',
          'fontWeight': 'normal'
        }
      },
      'markers': {
        'size': markers
      },
      'fill': {
        'type': 'solid'
      },
      'stroke': stroke,
      'chart': {
        'animations': {
          'enabled': False
        },
        'toolbar': {
          'show': False
        },
        'zoom': {
          'enabled': False
        }
      }
    }

    return config
