import struct
import unittest
from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants

# header para
MESSAGEID = 0x04
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0

# payload para
MonitorData_No = 1
Reserved = 0

SatelliteNo = 0
GPSStatus = 0
LongitudeDu = 121
LongitudeFen = 2
LongitudeMiao = 34
LongitudeQuadrant = 'E'
LatitudeDu = 23
LatitudeFen = 4
LatitudeMiao = 56
LatitudeQuadrant = "N"
Direction = 0
IntSpeed = 0
Year = 22
Month = 3
Day = 23
Hour = 19
Minute = 6
Second = 2

gps_strct_pdu = struct.pack(
    '<BBBBH1sBBH1sHHBBBBBB', SatelliteNo, GPSStatus,
    LongitudeDu, LongitudeFen, LongitudeMiao, LongitudeQuadrant.encode(),
    LatitudeDu, LatitudeFen, LatitudeMiao, LatitudeQuadrant.encode(),
    Direction, IntSpeed,
    Year, Month, Day, Hour, Minute, Second
)

AvgSpeed = struct.pack(
    '<H', 40,
)
IntSpeed_pdu = bytes()
RPMs_pdu = bytes()
IntSpeeds = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40]
RPMs = [s + 20 for s in IntSpeeds]

for s in IntSpeeds:
    IntSpeed_pdu += struct.pack('<H', s)

for r in RPMs:
    RPMs_pdu += struct.pack('<H', r)

MonitorDataType1_pdu_1 = gps_strct_pdu + AvgSpeed + IntSpeed_pdu + RPMs_pdu + struct.pack('<BBI', 0x02, 0x08, 80)

payload_pdu = struct.pack('<BB', MonitorData_No+1, Reserved) + MonitorDataType1_pdu_1 + MonitorDataType1_pdu_1

HEADER_PDU = struct.pack(
    '<4sBBHHBIHBH',
    bytearray(MessageConstants.ProtocolID.encode('ascii')),
    MessageConstants.ProtocolVer,
    MESSAGEID,
    CustomerID,
    CarID,
    1,
    head_DriverID,
    65535,  # Sequence
    head_Reserved,
    len(payload_pdu)  # Len
)

pdu_pack = HEADER_PDU + payload_pdu


class TestMonitorUplink(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()
