import struct
import unittest

from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants


# header para
MESSAGEID = 0xF2
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0

# payload
record1_pdu = struct.pack('<BB', 1, 1)
record2_pdu = struct.pack('<BB', 2, 1)
record3_pdu = struct.pack('<BB', 3, 1)
record4_pdu = struct.pack('<BB', 4, 1)

t1 = struct.pack('<6B', 22, 3, 23, 0, 0, 0)
t2 = struct.pack('<6B', 22, 3, 24, 0, 0, 0)

OD_struct = struct.pack('<BB', 6, 5) + t1 + t2 + struct.pack('BB', 5, 4) \
           + record1_pdu + record2_pdu + record3_pdu + record4_pdu

payload_pdu = struct.pack('<HB1sBB', 256, 0, 'a'.encode(), 2, 0) + OD_struct + OD_struct


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


class TestODReportUplink(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()
