import struct
from ..message_base import MessageBase
from ..tables.MonitorStruct import MonitorStructType1


class MonitorDownlink(MessageBase):
    MessageID = 0x05

    def __init__(self, init_data, init_type: str):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        pass

    def to_pdu(self) -> bytes:
        pass

    def from_dict(self, input_dict: dict):
        pass

    def to_dict(self) -> dict:
        return {}

    def from_default(self):
        pass