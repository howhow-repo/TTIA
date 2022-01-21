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
        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        return struct.pack('<HBB', self.MsgTag, self.MsgStatus, self.Reserved)

    def from_dict(self, input_dict):
        self.MsgTag = input_dict['MsgTag']
        self.MsgStatus = input_dict['MsgStatus']
        self.Reserved = input_dict['Reserved']
        self.self_assert()

    def to_dict(self):
        self.self_assert()
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

    def self_assert(self):
        assert self.MsgStatus in [0, 1], "MsgStatus should be 0~1; 0:訊息設定失敗 1:訊息設定成功"
