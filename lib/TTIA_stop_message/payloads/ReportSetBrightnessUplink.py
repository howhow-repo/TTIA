import struct
from .payload_base import PayloadBase


class ReportSetBrightnessUplink(PayloadBase):
    message_id = 0x0E
    message_cname = "亮度設定確認"

    def from_pdu(self, pdu):
        pass

    def to_pdu(self):
        return b''

    def from_dict(self, input_dict):
        pass

    def to_dict(self):
        r = {}
        return r

    def from_default(self):
        pass
