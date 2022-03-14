import struct
from ..EventCode import EventCode
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class DoorOpenOnDriving(MessageBase):
    EventCode = EventCode.DoorOpenOnDriving

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.Type = 0
        self.Reserved = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<BB', pdu[30:])
        self.Type = payload[0]
        self.Reserved = payload[1]

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData + struct.pack('<BB',  self.Type, self.Reserved)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.Type = input_dict['Type']
        self.Reserved = input_dict['Reserved']

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'Type': self.Type,
            'Reserved': self.Reserved
        }
        return r

    def from_default(self):
        pass
