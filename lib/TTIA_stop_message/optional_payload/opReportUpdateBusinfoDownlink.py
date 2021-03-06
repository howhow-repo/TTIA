import struct
from .op_payload_base import OpPayloadBase


class OpReportUpdateBusinfoDownlink(OpPayloadBase):
    message_id = 0x07

    def __init__(self, init_data, init_type):
        self.SpectialEstimateTime = 0
        self.MsgCContent = ''
        self.MsgEContent = ''
        self.RouteMsgCContent = ''
        self.RouteMsgEContent = ''
        self.VoiceAlertMode = 0
        self.Sequence = 0
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
        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        MsgCContent = bytearray(self.MsgCContent.encode("big5"))
        MsgEContent = bytearray(self.MsgEContent.encode("ascii"))
        assert len(MsgCContent) <= 12, f"MsgCContent: [{self.MsgCContent}] overflow, please make sure it beneath 12 bytes"
        assert len(MsgEContent) <= 12, f"MsgEContent [{self.MsgEContent}] overflow, please make sure it beneath 12 bytes"

        RouteMsgCContent = bytearray(self.RouteMsgCContent.encode("big5"))
        RouteMsgEContent = bytearray(self.RouteMsgEContent.encode("ascii"))
        assert len(RouteMsgCContent) <= 24, "RouteMsgCContent overflow, please make sure it beneath 24 bytes"
        assert len(RouteMsgEContent) <= 24, "RouteMsgEContent overflow, please make sure it beneath 24 bytes"

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
        self.self_assert()

    def to_dict(self):
        self.self_assert()
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
        pass

    def self_assert(self):
        assert self.SpectialEstimateTime in range(0, 8), \
            "SpectialEstimateTime should be 0~8; " \
            "0:??????(???EstimateTime?????????????????????  1:???????????? 2:??????????????? 3:??????????????? 4:??????????????? 5:????????? 6:???????????? 7:???????????? 8:???????????????????????????"
        assert self.VoiceAlertMode in [0, 1], \
            "VoiceAlertMode should be 0 or 1; 0:???????????? 1:???????????? (????????????[???????????? ????????????< 180???])"
