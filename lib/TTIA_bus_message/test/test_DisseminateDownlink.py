import struct
import unittest

from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants


# header para
MESSAGEID = 0xE0
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0

# payload
MsgNum = 3
c1_str_pdu = "第一則訊息".encode('big5')
c1 = struct.pack('<BB', 1, len(c1_str_pdu)) + c1_str_pdu

c2_str_pdu = "第2則訊息".encode('big5')
c2 = struct.pack('<BB', 2, len(c2_str_pdu)) + c2_str_pdu

c3_str_pdu = "第3則訊息".encode('big5')
c3 = struct.pack('<BB', 3, len(c3_str_pdu)) + c3_str_pdu

payload_pdu = struct.pack('<B', MsgNum) + c1 + c2 + c3

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


class TestDisseminateDownlink(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()
