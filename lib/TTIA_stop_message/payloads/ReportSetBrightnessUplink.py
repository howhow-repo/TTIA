import struct
from .payload_base import PayloadBase


class ReportSetBrightnessUplink(PayloadBase):
    message_id = 0x0E

    def from_pdu(self, pdu):
        pass

    def to_pdu(self):
        return b''

    def from_dict(self, json):
        pass

    def to_dict(self):
        r = {}
        return r

    def from_default(self):
        pass