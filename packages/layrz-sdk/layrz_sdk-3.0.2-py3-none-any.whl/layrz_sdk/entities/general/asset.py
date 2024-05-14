""" Asset Entity """
from .asset_operation_mode import AssetOperationMode
from .custom_field import CustomField
from .device import Device
from .sensor import Sensor


class Asset:
  """
  Asset entity definition
  ---
  Attributes
    - pk : Asset ID
    - name : Name of the asset
    - vin : Vehicle identification number
    - plate : Vehicle plate number
    - asset_type : Asset type ID
    - devices : List of devices
    - operation_mode : Operation mode of the asset
    - custom_fields : List of custom fields
    - children : List of children assets
    - sensors : List of sensors
  """

  def __init__(
    self,
    pk: int,
    name: str,
    vin: str,
    plate: str,
    asset_type: int,
    operation_mode: AssetOperationMode,
    sensors: list[Sensor] = None,
    custom_fields: list[CustomField] = None,
    devices: list[Device] = None,
    children: list = None,
  ):
    """ Constructor """
    self.pk = pk
    self.name = name
    self.vin = vin
    self.plate = plate
    self.asset_type = asset_type
    self.operation_mode = operation_mode
    self.sensors = sensors if sensors else []
    self.custom_fields = custom_fields if custom_fields else []
    self.devices = devices if devices else []
    self.children = children if children else []

  @property
  def _readable(self) -> str:
    """ Readable """
    return f'Asset(pk={self.pk}, name={self.name}, vin={self.vin}, plate={self.plate}, ' +\
           f'asset_type={self.asset_type}, operation_mode={self.operation_mode}, ' +\
           f'custom_fields={self.custom_fields}, children={self.children}, sensors={self.sensors})'

  def __str__(self) -> str:
    """ Readable property """
    return self._readable

  def __repr__(self) -> str:
    """ Readable property """
    return self._readable
