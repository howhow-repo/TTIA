import struct
from .payload_base import PayloadBase


class ReportMsgcountUplink(PayloadBase):
    message_id = 0x03
    message_cname = "定時回報訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        header = struct.unpack_from('<HH', pdu)
        self.SentCount = header[0]
        self.RecvCount = header[1]

    def to_pdu(self):
        return struct.pack('<HH', self.SentCount, self.RecvCount)

    def from_dict(self, json):
        self.SentCount = json['SentCount']
        self.RecvCount = json['RecvCount']

    def to_dict(self):
        r = {
            'SentCount': self.SentCount,
            'RecvCount': self.RecvCount,
        }
        return r

    def from_default(self):
        self.SentCount = 0
        self.RecvCount = 0
