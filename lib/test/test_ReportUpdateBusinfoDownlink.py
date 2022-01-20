import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x07
Provider = 65535

RouteID = 12
BusID = 66
CurrentStop = 15
DestinationStop = 19
IsLastBus = 0
EstimateTime=6000
StopDistance = 5678
Direction = 2
Type = 1
TransYear = 2022
TransMonth = 3
TransDay = 9
TransHour = 16
TransMinute = 5
TransSecond = 40
RcvYear = 2022
RcvMonth = 3
RcvDay = 9
RcvHour = 16
RcvMinute = 5
RcvSecond = 45
Reserved = 0



SpectialEstimateTime = 0
MsgCContent = '我是中文'
MsgEContent = "im english"
RouteMsgCContent = "我是中文2"
RouteMsgEContent = "im english too"
VoiceAlertMode = 0
Sequence = 0

payload = struct.pack('<HHQQBHHBBBBBBBBBBBBBBB', RouteID, BusID, CurrentStop,
                           DestinationStop, IsLastBus, EstimateTime, StopDistance,
                           Direction,
                           Type, TransYear - 2000, TransMonth, TransDay, TransHour,
                           TransMinute, TransSecond,
                           RcvYear - 2000, RcvMonth, RcvDay, RcvHour, RcvMinute,
                           RcvSecond, Reserved,
                           )

option_payload = struct.pack('<B12s12s24s24sBH', SpectialEstimateTime,
                           MsgCContent.encode("big5"), MsgEContent.encode(), RouteMsgCContent.encode("big5"),
                           RouteMsgEContent.encode(), VoiceAlertMode, Sequence
                           )

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload + option_payload


class TestReportUpdateBusinfoDownlink(unittest.TestCase):
    def test_from_to_pdu_by_raw_pdu(self):
        msg = TTIABusStopMessage(init_data=pdu_pack, init_type='pdu')
        self.assertEqual(msg.to_pdu(), pdu_pack)

    def test_from_to_dict_by_default_creation(self):
        default_msg = TTIABusStopMessage(init_data=MESSAGEID, init_type='default')
        obj_dict = default_msg.to_dict()
        from_dict_msg = TTIABusStopMessage(init_data=obj_dict, init_type='dict')
        self.assertEqual(from_dict_msg.to_dict(), obj_dict)

    def test_from_to_pdu_by_default_creation(self):
        default_msg = TTIABusStopMessage(init_data=MESSAGEID, init_type='default')
        msg = TTIABusStopMessage(init_data=default_msg.to_pdu(), init_type='pdu')
        self.assertEqual(msg.to_pdu(), default_msg.to_pdu())
        self.assertEqual(msg.to_dict(), default_msg.to_dict())
