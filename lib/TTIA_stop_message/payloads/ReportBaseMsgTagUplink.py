import struct
from .payload_base import PayloadBase


class ReportBaseMsgTagUplink(PayloadBase):
    message_id = 0x02
    message_cname = "基本資料設定確認訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HBB', pdu)
        self.MsgTag = payload[0]
        self.MsgStatus = payload[1]
        self.Reserved = payload[2]

    def to_pdu(self):
        return struct.pack('<HBB', self.MsgTag, self.MsgStatus, self.Reserved)

    def from_dict(self, input_dict):
        self.MsgTag = input_dict['MsgTag']
        self.MsgStatus = input_dict['MsgStatus']
        self.Reserved = input_dict['Reserved']

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
