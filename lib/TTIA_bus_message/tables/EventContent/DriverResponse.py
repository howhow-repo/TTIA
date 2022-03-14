import struct
from ..EventCode import EventCode
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class DriverResponse(MessageBase):
    EventCode = EventCode.DriverResponse

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.InfoID = 0
        self.Type = 0
        self.Reserved = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<HBB', pdu[30:])
        self.InfoID = payload[0]
        self.Type = payload[1]
        self.Reserved = payload[2]

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData + struct.pack('<HBB', self.InfoID, self.Type, self.Reserved)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.InfoID = input_dict['InfoID']
        self.Type = input_dict['Type']
        self.Reserved = input_dict['Reserved']

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'InfoID': self.InfoID,
            'Type': self.Type,
            'Reserved': self.Reserved
        }
        return r

    def from_default(self):
        pass
