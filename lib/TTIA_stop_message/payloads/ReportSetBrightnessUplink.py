import struct
from .payload_base import PayloadBase


class ReportSetBrightnessUplink(PayloadBase):
    message_id = 0x0E
    message_cname = "亮度設定確認"

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
