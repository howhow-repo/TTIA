import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestBaseCase


MESSAGEID = 0x13
Provider = 65535

payload = b''

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestReportUpdateGifUplink(TestBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
