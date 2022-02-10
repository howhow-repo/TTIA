import struct
from .payload_base import PayloadBase


class ReportMsgcountUplink(PayloadBase):
    message_id = 0x03
    message_cname = "定時回報訊息"

    def __init__(self, init_data, init_type):
        self.SentCount = 0
        self.RevCount = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        header = struct.unpack_from('<HH', pdu)
        self.SentCount = header[0]
        self.RevCount = header[1]

    def to_pdu(self) -> bytes:
        return struct.pack('<HH', self.SentCount, self.RevCount)

    def from_dict(self, input_dict: dict):
        self.SentCount = input_dict['SentCount']
        self.RevCount = input_dict['RevCount']

    def to_dict(self) -> dict:
        r = {
            'SentCount': self.SentCount,
            'RevCount': self.RevCount,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
