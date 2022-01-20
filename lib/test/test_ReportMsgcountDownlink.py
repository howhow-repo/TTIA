import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestBaseCase


MESSAGEID = 0x04
Provider = 65535
IMSI = 'IMSI123456'
IMEI = 'IMEI7891'

payload = b''

option_payload = b''

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len


pdu_pack = HEADER_PDU + payload


class TestReportMsgcountDownlink(TestBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
