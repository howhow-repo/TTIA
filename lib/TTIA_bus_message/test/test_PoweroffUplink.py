import struct
import unittest

from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants


# header para
MESSAGEID = 0x0A
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0


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
moniter2_data_pdu = gps_strct_pdu + struct.pack("<HBBI", AvgSpeed, 1, 1, 60)

payload_pdu = moniter2_data_pdu + struct.pack("<HBB", 30000, 50, 60)

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


class TestPoweroffUplink(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()