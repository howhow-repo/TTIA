import struct
from .payload_base import PayloadBase


class ReportAbnormalDownlink(PayloadBase):
    message_id = 0x0A
    message_cname = "異常回報確認訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<BB', pdu)
        self.MsgStatus = payload[0]
        self.Reserved = payload[1]

        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        return struct.pack('<BB', self.MsgStatus, self.Reserved)

    def from_dict(self, input_dict):
        self.MsgStatus = input_dict['MsgStatus']
        self.Reserved = input_dict['Reserved']

        self.self_assert()

    def to_dict(self):
        self.self_assert()
        r = {
            'MsgStatus': self.MsgStatus,
            'Reserved': self.Reserved
        }
        return r

    def from_default(self):
        self.MsgStatus = 1
        self.Reserved = 0

    def self_assert(self):
        assert self.MsgStatus in [0, 1], "MsgStatus should be 0~1; 0:fail 1:success"
