import struct
from .payload_base import PayloadBase


class ReportUpdateMsgTagDownlink(PayloadBase):
    message_id = 0x05

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HH160s', pdu)
        self.MsgTag = payload[0]
        self.MsgNo = payload[1]
        self.MsgContent = payload[2].decode('big5')

    def to_pdu(self):
        MsgContent = bytearray(self.MsgContent.encode("big5"))
        return struct.pack('<HH160s', self.MsgTag, self.MsgNo, MsgContent)

    def from_dict(self, json):
        self.MsgTag = json['MsgTag']
        self.MsgNo = json['MsgNo']
        self.MsgContent = json['MsgContent']

    def to_dict(self):
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
