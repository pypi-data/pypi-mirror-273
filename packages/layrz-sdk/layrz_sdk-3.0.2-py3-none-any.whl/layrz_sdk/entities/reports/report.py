""" Report class """
import os
import time
import warnings

import xlsxwriter

from layrz_sdk.helpers.color import use_black

from .col import ReportDataType
from .format import ReportFormat
from .page import CustomReportPage, ReportPage


class Report:
  """
  Report definition
  ---
  Attributes
    - name : Report name. The exported name will have an timestamp to prevent duplicity in our servers.
    - pages : List of pages to append into report
    - export_format : Format to export the report
  """

  def __init__(
    self,
    name: str,
    pages: list[ReportPage | CustomReportPage],
    export_format: ReportFormat = None,
  ) -> None:
    self.name = name
    self.pages = pages

    if export_format is not None:
      warnings.warn('export_format is deprecated, submit the export format in the `export()` method instead',
                    DeprecationWarning)

    self.export_format = export_format

  @property
  def filename(self) -> str:
    """ Report filename """
    return f'{self.name}_{int(time.time() * 1000)}.xlsx'

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'Report(name={self.name}, pages={len(self.pages)})'

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def export(self, path, export_format: ReportFormat = None) -> str:
    """ Export report to file """
    if export_format:
      if export_format == ReportFormat.MICROSOFT_EXCEL:
        return self._export_xlsx(path)
      elif export_format == ReportFormat.JSON:
        return self._export_json()
      else:
        raise AttributeError(f'Unsupported export format: {export_format}')

    if self.export_format == ReportFormat.MICROSOFT_EXCEL:
      return self._export_xlsx(path)
    elif self.export_format == ReportFormat.JSON:
      return self._export_json()
    else:
      raise AttributeError(f'Unsupported export format: {self.export_format}')

  def export_as_json(self) -> dict:
    """ Returns the report as a JSON dict"""
    return self._export_json()

  def _export_json(self) -> dict:
    """ Returns a JSON dict of the report"""
    json_pages = []
    for page in self.pages:
      headers = []
      for header in page.headers:
        headers.append({
          'content': header.content,
          'text_color': '#000000' if use_black(header.color) else '#ffffff',
          'color': header.color,
        })
      rows = []
      for row in page.rows:
        cells = []
        for cell in row.content:
          cells.append({
            'content': cell.content,
            'text_color': '#000000' if use_black(cell.color) else '#ffffff',
            'color': cell.color,
            'data_type': cell.data_type.value,
          })
        rows.append({
          'content': cells,
          'compact': row.compact,
        })
      json_pages.append({
        'name': page.name,
        'headers': headers,
        'rows': rows,
      })

    return {
      'name': self.name,
      'pages': json_pages,
    }

  def _export_xlsx(self, path) -> str:
    """ Export to Microsoft Excel (.xslx) """

    full_path = os.path.join(path, self.filename)
    book = xlsxwriter.Workbook(full_path)

    for page in self.pages:
      sheet_name = page.name[0:31]

      # Allow only numbers, letters, spaces and _ or - characters
      # Other characters will be removed
      sheet_name = ''.join(e for e in sheet_name if e.isalnum() or e in [' ', '_', '-'])
      sheet = book.add_worksheet(sheet_name)

      if isinstance(page, CustomReportPage):
        page.builder(sheet)
        sheet.autofit()
        continue

      if page.freeze_header:
        sheet.freeze_panes(1, 0)

      for i, header in enumerate(page.headers):
        style = book.add_format({
          'align': header.align.value,
          'font_color': '#000000' if use_black(header.color) else '#ffffff',
          'bg_color': header.color,
          'bold': header.bold,
          'valign': 'vcenter',
          'font_size': 11,
          'top': 1,
          'left': 1,
          'right': 1,
          'bottom': 1,
          'font_name': 'Aptos Narrow',
        })
        sheet.write(0, i, header.content, style)

      for i, row in enumerate(page.rows):
        for j, cell in enumerate(row.content):
          style = {
            'align': cell.align.value,
            'font_color': '#000000' if use_black(cell.color) else '#ffffff',
            'bg_color': cell.color,
            'bold': cell.bold,
            'valign': 'vcenter',
            'font_size': 11,
            'top': 1,
            'left': 1,
            'right': 1,
            'bottom': 1,
            'font_name': 'Aptos Narrow',
          }

          if cell.data_type == ReportDataType.BOOL:
            value = 'Yes' if cell.value else 'No'
          elif cell.data_type == ReportDataType.DATETIME:
            value = cell.content.strftime(cell.datetime_format)
          elif cell.data_type == ReportDataType.INT:
            value = int(cell.content)
          elif cell.data_type == ReportDataType.FLOAT:
            value = float(cell.content)
            style.update({'num_format': '0.00'})
          elif cell.data_type == ReportDataType.CURRENCY:
            value = float(cell.content)
            style.update(
              {'num_format': f'"{cell.currency_symbol}" * #,##0.00;[Red]"{cell.currency_symbol}" * #,##0.00'})
          else:
            value = cell.content

          sheet.write(i + 1, j, value, book.add_format(style))

          if row.compact:
            sheet.set_row(i + 1, None, None, {'level': 1, 'hidden': True})
          else:
            sheet.set_row(i + 1, None, None, {'collapsed': True})

      sheet.autofit()
    book.close()

    return full_path


class ReportConfiguration:
  """ 
  Report Configuration class
  ---
  Attributes
    - title : Report title
    - pages_count : Number of pages in the report
  """

  def __init__(self, title: str, pages_count: int) -> None:
    self.title = title
    self.pages_count = pages_count

  @property
  def _readable(self) -> str:
    """ Readable property """
    return f'ReportConfiguration(title={self.title}, pages_count={self.pages_count})'

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable

  def __str__(self) -> str:
    """ Readable property """
    return self._readable
