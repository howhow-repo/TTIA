import struct
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class DutyOnNotSchedule(MessageBase):

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.Movement = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<H', pdu[30:])
        self.Movement = payload[0]

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData + struct.pack('<H',  self.Movement)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.Movement = input_dict['Movement']

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'Movement': self.Movement,
        }
        return r

    def from_default(self):
        pass
