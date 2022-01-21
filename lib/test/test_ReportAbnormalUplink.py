import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestBaseCase

MESSAGEID = 0x09
Provider = 65535
IMSI = 'IMSI123456'
IMEI = 'IMEI7891'

StatusCode = 1
Type = 1
TransYear = 2021
TransMonth = 1
TransDay = 1
TransHour = 1
TransMinute = 0
TransSecond = 0
RcvYear = 2021
RcvMonth = 5
RcvDay = 5
RcvHour = 6
RcvMinute = 15
RcvSecond = 15

payload = struct.pack('<BBBBBBBBBBBBBB',
                           StatusCode,
                           Type,
                           TransYear - 2000,
                           TransMonth,
                           TransDay,
                           TransHour,
                           TransMinute,
                           TransSecond,
                           RcvYear - 2000,
                           RcvMonth,
                           RcvDay,
                           RcvHour,
                           RcvMinute,
                           RcvSecond)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len


pdu_pack = HEADER_PDU + payload


class TestReportAbnormalUplink(TestBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
