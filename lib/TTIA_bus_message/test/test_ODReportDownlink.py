import struct
import unittest

from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants


# header para
MESSAGEID = 0xF3
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0

payload_pdu = b''


HEADER_PDU = struct.pack('<4sBBHHBIHBH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         CustomerID,
                         CarID,
                         1,
                         head_DriverID,
                         65535,  # Sequence
                         head_Reserved,
                         len(payload_pdu))  # Len

pdu_pack = HEADER_PDU + payload_pdu


class TestODReportDownlink(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()
