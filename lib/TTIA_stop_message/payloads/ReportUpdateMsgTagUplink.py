import struct
from .payload_base import PayloadBase


class ReportUpdateMsgTagUplink(PayloadBase):
    message_id = 0x06
    message_cname = "更新站牌文字確認訊息"

    def __init__(self, init_data, init_type, buff=None, offset=0):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HHBB', pdu)
        self.MsgTag = payload[0]
        self.MsgNo = payload[1]
        self.MsgStatus = payload[2]
        self.Reserved = payload[3]

    def to_pdu(self):
        return struct.pack('<HHBB', self.MsgTag, self.MsgNo, self.MsgStatus, self.Reserved)

    def from_dict(self, json):
        self.MsgTag = json['MsgTag']
        self.MsgNo = json['MsgNo']
        self.MsgStatus = json['MsgStatus']
        self.Reserved = json['Reserved']

    def to_dict(self):
        r = {
            'MsgTag': self.MsgTag,
            'MsgNo': self.MsgNo,
            'MsgStatus': self.MsgStatus,
            'Reserved': self.Reserved
        }
        return r

    def from_default(self):
        self.MsgTag = 0
        self.MsgNo = 0
        self.MsgStatus = 0
        self.Reserved = 0
