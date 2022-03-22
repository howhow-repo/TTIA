import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestStopMsgBaseCase


MESSAGEID = 0x0B
Provider = 65535

RouteID = 0
PathCName = '中文站名'
PathEName = 'stop eng name'
Sequence = 0


payload = struct.pack('<H12s12sH',
                      RouteID, bytearray(PathCName.encode('big5')),
                      bytearray(PathEName.encode('ascii')),
                      Sequence)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestReportUpdateRouteinfoDownlink(TestStopMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
