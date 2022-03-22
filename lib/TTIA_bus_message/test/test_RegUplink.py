import struct
import unittest

from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants

MESSAGEID = 0x00
CustomerID = 65535
CarID = 60000
DriverID = 123456
IDStorage = 1
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

AvgSpeed = 40
IntSpeed = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]
RPM = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

IntSpeed_l = bytes()
RPM_l = bytes()

for speed in IntSpeed:
    IntSpeed_l += struct.pack('<H', speed)
for R in RPM:
    RPM_l += struct.pack('<H', R)

moniter2_data_pdu = gps_strct_pdu + struct.pack("<HBBI", AvgSpeed, 1, 1, 60)

fileinfo1_pdu = struct.pack("<4s6s", 'filename1'.encode(), '220320'.encode())
fileinfo2_pdu = struct.pack("<4s6s", 'filename2'.encode(), '220321'.encode())

IMSI = 'IMSIIMSIIMSI'.encode()
IMCI = 'IMCIIMCIIMCI'.encode()

payload_pdu = moniter2_data_pdu + struct.pack('<15s15sBQBBB', IMSI, IMCI, 1, 123, 0, 2, 2) + fileinfo1_pdu + fileinfo2_pdu

HEADER_PDU = struct.pack('<4sBBHHBIHBH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         CustomerID,
                         CarID,
                         1,
                         DriverID,
                         65535,  # Sequence
                         Reserved,
                         len(payload_pdu))  # Len

pdu_pack = HEADER_PDU + payload_pdu


class TestBusMsgRegUPLINK(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()
