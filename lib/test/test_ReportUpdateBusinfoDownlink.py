import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestBaseCase


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


class TestReportUpdateBusinfoDownlink(TestBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
