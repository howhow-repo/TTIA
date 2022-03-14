import struct
from ..EventCode import EventCode
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class StopEnterLeave(MessageBase):
    EventCode = EventCode.StopEnterLeave

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.StationID = 0
        self.Type = 0
        self.DoorOpen = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<HBB', pdu[30:])
        self.StationID = payload[0]
        self.Type = payload[1]
        self.DoorOpen = payload[2]

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData + struct.pack('<HBB', self.StationID, self.Type, self.DoorOpen)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.StationID = input_dict['StationID']
        self.Type = input_dict['Type']
        self.DoorOpen = input_dict['DoorOpen']

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'StationID': self.StationID,
            'Type': self.Type,
            'DoorOpen': self.DoorOpen
        }
        return r

    def from_default(self):
        pass

