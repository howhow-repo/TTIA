import struct
from ..message_base import MessageBase


class GPSStruct(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.SatelliteNo = 0
        self.GPSStatus = 0
        self.LongitudeDu = 0
        self.LongitudeFen = 0
        self.LongitudeMiao = 0
        self.LongitudeQuadrant = 0
        self.LatitudeDu = 0
        self.LatitudeFen = 0
        self.LatitudeMiao = 0
        self.LatitudeQuadrant = 0
        self.Direction = 0
        self.IntSpeed = 0
        self.Year = 2000
        self.Month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0

        super().__init__(init_data, init_type)

    def from_pdu(self, pdu, offset=0):
        pdu = struct.unpack('<BBBBHBBBHBHHBBBBBB', pdu)
        self.SatelliteNo = pdu[0]
        self.GPSStatus = pdu[1]
        self.LongitudeDu = pdu[2]
        self.LongitudeFen = pdu[3]
        self.LongitudeMiao = pdu[4]
        self.LongitudeQuadrant = pdu[5]
        self.LatitudeDu = pdu[6]
        self.LatitudeFen = pdu[7]
        self.LatitudeMiao = pdu[8]
        self.LatitudeQuadrant = pdu[9]

        self.Direction = pdu[10]
        self.IntSpeed = pdu[11]
        self.Year = pdu[12] + 2000
        self.Month = pdu[13]
        self.Day = pdu[14]
        self.Hour = pdu[15]
        self.Minute = pdu[16]
        self.Second = pdu[17]

    def to_pdu(self):
        return struct.pack('<BBBBHBBBHBHHBBBBBB', self.SatelliteNo, self.GPSStatus,
                           self.LongitudeDu, self.LongitudeFen, self.LongitudeMiao, self.LongitudeQuadrant,
                           self.LatitudeDu, self.LatitudeFen, self.LatitudeMiao, self.LatitudeQuadrant,
                           self.Direction, self.IntSpeed,
                           self.Year - 2000, self.Month, self.Day, self.Hour, self.Minute, self.Second)

    def from_dict(self, input_dict):
        self.SatelliteNo = input_dict['SatelliteNo']
        self.GPSStatus = input_dict['GPSStatus']
        self.LongitudeDu = input_dict['LongitudeDu']
        self.LongitudeFen = input_dict['LongitudeFen']
        self.LongitudeMiao = input_dict['LongitudeMiao']
        self.LongitudeQuadrant = input_dict['LongitudeQuadrant']
        self.LatitudeDu = input_dict['LatitudeDu']
        self.LatitudeFen = input_dict['LatitudeFen']
        self.LatitudeMiao = input_dict['LatitudeMiao']
        self.LatitudeQuadrant = input_dict['LatitudeQuadrant']
        self.Direction = input_dict['Direction']
        self.IntSpeed = input_dict['IntSpeed']
        self.Year = input_dict['Year']
        self.Month = input_dict['Month']
        self.Day = input_dict['Day']
        self.Hour = input_dict['Hour']
        self.Minute = input_dict['Minute']
        self.Second = input_dict['Second']

    def to_dict(self):
        r = {
            'SatelliteNo': self.SatelliteNo,
            'GPSStatus': self.GPSStatus,
            'LongitudeDu': self.LongitudeDu,
            'LongitudeFen': self.LongitudeFen,
            'LongitudeMiao': self.LongitudeMiao,
            'LongitudeQuadrant': self.LongitudeQuadrant,
            'LatitudeDu': self.LatitudeDu,
            'LatitudeFen': self.LatitudeFen,
            'LatitudeMiao': self.LatitudeMiao,
            'LatitudeQuadrant': self.LatitudeQuadrant,
            'Direction': self.Direction,
            'IntSpeed': self.IntSpeed,
            'Year': self.Year,
            'Month': self.Month,
            'Day': self.Day,
            'Hour': self.Hour,
            'Minute': self.Minute,
            'Second': self.Second,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        assert 2000 <= self.Year, "Year must > 2000"
        assert 1 <= self.Month <= 12, "Month range error"
        assert 1 <= self.Day <= 31, "Day range error"
        assert 0 <= self.Hour <= 23, "Hour range error"
        assert 0 <= self.Minute <= 59, "Min range error"
        assert 0 <= self.Second <= 59, "Sec range error"
