import struct
from .payload_base import PayloadBase


class ReportUpdateGifUplink(PayloadBase):
    message_id = 0x13

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