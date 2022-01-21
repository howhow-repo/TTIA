import struct
from .payload_base import PayloadBase


class ReportUpdateGifUplink(PayloadBase):
    message_id = 0x13
    message_cname = "動態圖示確認訊息"

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