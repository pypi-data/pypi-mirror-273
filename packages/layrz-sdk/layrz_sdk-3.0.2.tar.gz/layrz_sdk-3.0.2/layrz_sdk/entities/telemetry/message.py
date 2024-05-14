""" Message entity """
from datetime import datetime

from .position import Position


class Message:
  """
  Message definition
  ---
  Attributes
    - pk : Message ID
    - asset_id : Asset ID
    - position : Geographic position
    - payload : Message raw payload
    - sensors : Calculated sensor values
    - received_at : Message reception date and time
  """

  def __init__(
    self,
    pk: int,
    asset_id: int,
    position: Position = None,
    payload: dict = None,
    sensors: dict = None,
    received_at: datetime = None,
  ) -> None:
    """ Constructor """
    self.pk = pk
    self.asset_id = asset_id
    self.position = position or Position()
    self.payload = payload or {}
    self.sensors = sensors or {}
    self.received_at = received_at or datetime.now()
