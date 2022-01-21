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
        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        return struct.pack('<HHBB', self.MsgTag, self.MsgNo, self.MsgStatus, self.Reserved)

    def from_dict(self, input_dict):
        self.MsgTag = input_dict['MsgTag']
        self.MsgNo = input_dict['MsgNo']
        self.MsgStatus = input_dict['MsgStatus']
        self.Reserved = input_dict['Reserved']
        self.self_assert()

    def to_dict(self):
        self.self_assert()
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

    def self_assert(self):
        assert self.MsgStatus in [0, 1], "MsgStatus should be 0~1; 0:訊息更新失敗 1:訊息更新成功"
