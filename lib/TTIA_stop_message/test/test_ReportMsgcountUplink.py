import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestStopMsgBaseCase


MESSAGEID = 0x03
Provider = 65535

SentCount = 0
RecvCount = 0

payload = struct.pack('<HH',
                        SentCount,
                        RecvCount
                      )

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestReportMsgcountUplink(TestStopMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID