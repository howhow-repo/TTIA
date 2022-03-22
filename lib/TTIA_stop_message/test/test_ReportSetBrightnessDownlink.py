import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestStopMsgBaseCase


MESSAGEID = 0x0D
Provider = 65535

LightSet = 9


payload = struct.pack('<B', LightSet)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestReportSetBrightnessDownlink(TestStopMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID