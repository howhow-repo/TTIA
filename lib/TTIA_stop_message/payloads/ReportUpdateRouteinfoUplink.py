import struct
from .payload_base import PayloadBase


class ReportUpdateRouteinfoUplink(PayloadBase):
    message_id = 0x0C
    message_cname = "路線資料設定確認訊息"

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HBB', pdu)
        self.MsgTag = payload[0]
        self.MsgStatus = payload[1]
        self.Reserved = payload[2]

    def to_pdu(self):
        return struct.pack('<HBB', self.MsgTag, self.MsgStatus, self.Reserved)

    def from_dict(self, json):
        self.MsgTag = json['MsgTag']
        self.MsgStatus = json['MsgStatus']
        self.Reserved = json['Reserved']

    def to_dict(self):
        r = {
            'MsgTag': self.MsgTag,
            'MsgStatus': self.MsgStatus,
            'Reserved': self.Reserved,
        }
        return r

    def from_default(self):
        self.MsgTag = 0
        self.MsgStatus = 0
        self.Reserved = 0
