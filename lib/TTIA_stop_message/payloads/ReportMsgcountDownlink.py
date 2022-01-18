import struct
from .payload_base import PayloadBase


class ReportMsgcountDownlink(PayloadBase):
    message_id = 0x04

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        pass

    def to_pdu(self):
        return b''

    def from_json(self, json):
        pass

    def to_json(self):
        r = {}
        return r

    def from_default(self):
        pass
