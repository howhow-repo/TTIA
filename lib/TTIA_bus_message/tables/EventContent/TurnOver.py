from ..EventCode import EventCode
from ..MonitorStruct import MonitorStructType2
from ...message_base import MessageBase


class TurnOver(MessageBase):
    EventCode = EventCode.TurnOver

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')

    def to_pdu(self) -> bytes:
        MonitorData = self.MonitorData.to_pdu()
        return MonitorData

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')

    def to_dict(self) -> dict:
        r = {
            'MonitorData': self.MonitorData.to_dict(),
        }
        return r

    def from_default(self):
        pass
