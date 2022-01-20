import struct
from .payload_base import PayloadBase


class ReportUpdateBusinfoUplink(PayloadBase):
    message_id = 0x08
    message_cname = "更新即時公車資訊確認訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<BB', pdu)
        self.MsgStatus = payload[0]
        self.Reserved = payload[1]

    def to_pdu(self):
        return struct.pack('<BB', self.MsgStatus, self.Reserved)

    def from_dict(self, json):
        self.MsgStatus = json['MsgStatus']
        self.Reserved = json['Reserved']

    def to_dict(self):
        r = {
            'MsgStatus': self.MsgStatus,
            'Reserved': self.Reserved,
        }
        return r

    def from_default(self):
        self.MsgStatus = 0
        self.Reserved = 0
