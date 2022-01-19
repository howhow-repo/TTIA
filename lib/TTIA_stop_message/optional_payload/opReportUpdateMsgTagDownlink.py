import struct
from .op_payload_base import OpPayloadBase


class OpReportUpdateMsgTagDownlink(OpPayloadBase):
    message_id = 0x05

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<BBBB', pdu)
        self.MsgPriority = payload[0]
        self.MsgType = payload[1]
        self.MsgStopDelay = payload[2]
        self.MsgChangeDelay = payload[3]

    def to_pdu(self):
        return struct.pack('<BBBB',
                           self.MsgPriority,
                           self.MsgType,
                           self.MsgStopDelay,
                           self.MsgChangeDelay,
                           )

    def from_json(self, json):
        self.MsgPriority = json['MsgPriority']
        self.MsgType = json['MsgType']
        self.MsgStopDelay = json['MsgStopDelay']
        self.MsgChangeDelay = json['MsgChangeDelay']

    def to_json(self):
        r = {
            'MsgPriority': self.MsgPriority,
            'MsgType': self.MsgType,
            'MsgStopDelay': self.MsgStopDelay,
            'MsgChangeDelay': self.MsgChangeDelay,
        }
        return r

    def from_default(self):
        self.MsgPriority = 0
        self.MsgType = 0
        self.MsgStopDelay = 2
        self.MsgChangeDelay = 1
