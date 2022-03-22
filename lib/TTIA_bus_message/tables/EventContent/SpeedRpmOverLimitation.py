import struct
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class SpeedRpmOverLimitation(MessageBase):

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.StationID = 0
        self.Type = 0
        self.Value = 0
        self.Reserved = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<HBHB', pdu[30:])
        self.StationID = payload[0]
        self.Type = payload[1]
        self.Value = payload[2]
        self.Reserved = payload[3]

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData + struct.pack('<HBHB', self.StationID, self.Type, self.Value, self.Reserved)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.StationID = input_dict['StationID']
        self.Type = input_dict['Type']
        self.Value = input_dict['Value']
        self.Reserved = input_dict['Reserved']

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'StationID': self.StationID,
            'Type': self.Type,
            'Value': self.Value,
            'Reserved': self.Reserved
        }
        return r

    def from_default(self):
        pass