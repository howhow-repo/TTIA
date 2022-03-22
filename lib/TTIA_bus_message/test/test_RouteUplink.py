import struct
import unittest

from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants


# header para
MESSAGEID = 0x02
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0

# payload para
RouteID = 1234
RouteDirect = 3
RouteBranch = 'a'.encode()

payload_pdu = struct.pack(
    '<HB1s', RouteID, RouteDirect, RouteBranch,
)


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


class TestBusMsgRouteUplink(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()