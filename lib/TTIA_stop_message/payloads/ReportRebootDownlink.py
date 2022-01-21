import struct
from .payload_base import PayloadBase


class ReportRebootDownlink(PayloadBase):
    message_id = 0x10
    message_cname = "重開通知訊息(系統軟體重置)"

    def from_pdu(self, pdu: bytes):
        pass

    def to_pdu(self) -> bytes:
        return b''

    def from_dict(self, input_dict: dict):
        pass

    def to_dict(self) -> dict:
        r = {}
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
