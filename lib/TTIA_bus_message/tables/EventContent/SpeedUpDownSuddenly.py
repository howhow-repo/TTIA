import struct
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class SpeedUpDownSuddenly(MessageBase):

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.Type = 0
        self.Speed = 0
        self.Reserved = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<BHB', pdu[30:])
        self.Type = payload[0]
        self.Speed = payload[1]
        self.Reserved = payload[2]

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData + struct.pack('<BHB', self.Type, self.Speed, self.Reserved)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.Type = input_dict['Type']
        self.Speed = input_dict['Speed']
        self.Reserved = input_dict['Reserved']

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'Type': self.Type,
            'Speed': self.Speed,
            'Reserved': self.Reserved
        }
        return r

    def from_default(self):
        pass
