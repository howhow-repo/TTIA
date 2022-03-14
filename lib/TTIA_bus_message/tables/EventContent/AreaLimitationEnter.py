import struct
from ..EventCode import EventCode
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class AreaLimitationEnter(MessageBase):
    EventCode = EventCode.AreaLimitationEnter

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.RegionID = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<H', pdu[30:])
        self.RegionID = payload[0]

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData + struct.pack('<H',  self.RegionID)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.RegionID = input_dict['RegionID']

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'RegionID': self.RegionID,
        }
        return r

    def from_default(self):
        pass
