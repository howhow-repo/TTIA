import struct
from .op_payload_base import OpPayloadBase


class OpReportUpdateBusinfoDownlink(OpPayloadBase):
    message_id = 0x07

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<B12s12s24s24sBH', pdu)
        self.SpectialEstimateTime = payload[0]
        self.MsgCContent = bytearray(payload[1]).decode('big5').rstrip('\x00')
        self.MsgEContent = bytearray(payload[2]).decode('ascii').rstrip('\x00')
        self.RouteMsgCContent = bytearray(payload[3]).decode('big5').rstrip('\x00')
        self.RouteMsgEContent = bytearray(payload[4]).decode('ascii').rstrip('\x00')
        self.VoiceAlertMode = payload[5]
        self.Sequence = payload[6]

    def to_pdu(self):
        return struct.pack('<B12s12s24s24sBH', self.SpectialEstimateTime,
                           self.MsgCContent.encode("big5"),
                           self.MsgEContent.encode('ascii'),
                           self.RouteMsgCContent.encode("big5"),
                           self.RouteMsgEContent.encode('ascii'),
                           self.VoiceAlertMode,
                           self.Sequence,
                           )

    def from_dict(self, input_dict):
        self.SpectialEstimateTime = input_dict['SpectialEstimateTime']
        self.MsgCContent = input_dict['MsgCContent']
        self.MsgEContent = input_dict['MsgEContent']
        self.RouteMsgCContent = input_dict['RouteMsgCContent']
        self.RouteMsgEContent = input_dict['RouteMsgEContent']
        self.VoiceAlertMode = input_dict['VoiceAlertMode']
        self.Sequence = input_dict['Sequence']

    def to_dict(self):
        r = {
            'SpectialEstimateTime': self.SpectialEstimateTime,
            'MsgCContent': self.MsgCContent,
            'MsgEContent': self.MsgEContent,
            'RouteMsgCContent': self.RouteMsgCContent,
            'RouteMsgEContent': self.RouteMsgEContent,
            'VoiceAlertMode': self.VoiceAlertMode,
            'Sequence': self.Sequence,
        }
        return r

    def from_default(self):
        self.SpectialEstimateTime = 0
        self.MsgCContent = ''
        self.MsgEContent = ''
        self.RouteMsgCContent = ''
        self.RouteMsgEContent = ''
        self.VoiceAlertMode = 0
        self.Sequence = 0
