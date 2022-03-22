import struct
import unittest

from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants


# header para
MESSAGEID = 0x01
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0

# payload para
Result = 0
Schedule = 1
RouteID = 0
RouteDirect = 0
RouteBranch = 'aa'
RouteVer = 1
Reserved = 0
DriverID = 0
DriverName = '王大明'
DepartHr = 0
DepartMin = 0
Year = 2000
Month = 1
Day = 1
Hour = 0
Min = 0
Sec = 0
Event = 1
RPM = 3001
Accelerate = 31
Decelerate = 32
Halt = 11
InRadius = 5
OutRadius = 6
Movement = 11
OTATime = 1
OTAIP = 0
OTAPort = 0

payload_pdu = struct.pack(
    '<BBHB1sHHI8sBBBBBBBBHHBBBBBHBIH', Result, Schedule, RouteID, RouteDirect, RouteBranch.encode(), RouteVer,
    Reserved, DriverID, DriverName.encode('big5'), DepartHr, DepartMin,
    Year-2000, Month, Day, Hour, Min, Sec,
    Event, RPM, Accelerate, Decelerate, Halt, InRadius, OutRadius,
    Movement, OTATime, OTAIP, OTAPort,
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


class TestBusMsgRegDownLINK(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()
