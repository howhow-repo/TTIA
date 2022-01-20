import struct
import unittest
from .test_base_case import TestBaseCase
from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x00
Provider = 65535
IMSI = 'IMSI123456'
IMEI = 'IMEI7891'
FV1, FV2, FV3 = 5, 0, 1
Reserved = 0

payload = struct.pack('<15s15sBBBB',
                         bytearray(IMSI.encode('ascii')),
                         bytearray(IMEI.encode('ascii')),
                         FV1, FV2, FV3, Reserved)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len


pdu_pack = HEADER_PDU + payload


class TestREGUPLINK(TestBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
