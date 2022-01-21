import struct
from .payload_base import PayloadBase


class ReportUpdateMsgTagDownlink(PayloadBase):
    message_id = 0x05
    message_cname = "更新站牌文字訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<HH160s', pdu)
        self.MsgTag = payload[0]
        self.MsgNo = payload[1]
        self.MsgContent = payload[2].decode('big5').rstrip('\x00')
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        MsgContent = bytearray(self.MsgContent.encode("big5"))
        return struct.pack('<HH160s', self.MsgTag, self.MsgNo, MsgContent)

    def from_dict(self, input_dict: dict):
        self.MsgTag = input_dict['MsgTag']
        self.MsgNo = input_dict['MsgNo']
        self.MsgContent = input_dict['MsgContent']
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'MsgTag': self.MsgTag,
            'MsgNo': self.MsgNo,
            'MsgContent': self.MsgContent,
        }
        return r

    def from_default(self):
        self.MsgTag = 0
        self.MsgNo = 0
        self.MsgContent = ''

    def self_assert(self):
        pass
