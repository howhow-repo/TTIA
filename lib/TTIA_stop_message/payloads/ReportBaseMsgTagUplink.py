import struct
from .payload_base import PayloadBase


class ReportBaseMsgTagUplink(PayloadBase):
    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HBB', pdu)
        self.MsgTag = payload[0]
        self.MsgStatus = payload[1]
        self.Reserved = payload[2]

    def to_pdu(self):
        return struct.pack('<HBB', self.MsgTag, self.MsgStatus, self.Reserved)

    def from_json(self, json):
        self.MsgTag = json['MsgTag']
        self.MsgStatus = json['MsgStatus']
        self.Reserved = json['Reserved']

    def to_json(self):
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
