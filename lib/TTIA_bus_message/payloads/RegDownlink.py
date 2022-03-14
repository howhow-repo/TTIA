import struct
from ..message_base import MessageBase
from ..tables import EventCode


class RegDownlink(MessageBase):
    MessageID = 0x01

    def __init__(self, init_data, init_type: str):
        self.Result = 0
        self.Schedule = 1
        self.RouteID = 0
        self.RouteDirect = 0
        self.RouteBranch = ''
        self.RouteVer = 0
        self.Reserved = 0
        self.DriverID = 0
        self.DriverName = ''
        self.DepartHr = 0
        self.DepartMin = 0
        self.Year = 2000
        self.Month = 1
        self.Day = 1
        self.Hour = 0
        self.Min = 0
        self.Sec = 0
        self.Event = EventCode.Normal
        self.RPM = 3000
        self.Accelerate = 30
        self.Decelerate = 30
        self.Halt = 10
        self.InRadius = 4
        self.OutRadius = 5
        self.Movement = 10
        self.OTATime = 1
        self.OTAIP = 0
        self.OTAPort = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<BBHB1sHHI8sBBBBBBBBHHBBBBBHBIH', pdu)
        self.Result = payload[0]
        self.Schedule = payload[1]
        self.RouteID = payload[2]
        self.RouteDirect = payload[3]
        self.RouteBranch = payload[4].decode().rstrip('\0')
        self.RouteVer = payload[5]
        self.Reserved = payload[6]
        self.DriverID = payload[7]
        self.DriverName = payload[8].decode('big5').rstrip('\0')
        self.DepartHr = payload[9]
        self.DepartMin = payload[10]
        self.Year = payload[11] + 2000
        self.Month = payload[12]
        self.Day = payload[13]
        self.Hour = payload[14]
        self.Min = payload[15]
        self.Sec = payload[16]
        self.Event = payload[17]
        self.RPM = payload[18]
        self.Accelerate = payload[19]
        self.Decelerate = payload[20]
        self.Halt = payload[21]
        self.InRadius = payload[22]
        self.OutRadius = payload[23]
        self.Movement = payload[24]
        self.OTATime = payload[25]
        self.OTAIP = payload[26]
        self.OTAPort = payload[27]

        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        RouteBranch = self.RouteBranch.encode('big5')
        DriverName = self.DriverName.encode('big5')
        return struct.pack('<BBHB1sHHI8sBBBBBBBBHHBBBBBHBIH',
                           self.Result, self.Schedule, self.RouteID, self.RouteDirect,
                           RouteBranch, self.RouteVer, self.Reserved, self.DriverID, DriverName,
                           self.DepartHr, self.DepartMin,
                           self.Year-2000, self.Month, self.Day, self.Hour, self.Min, self.Sec,
                           self.Event, self.RPM, self.Accelerate, self.Decelerate, self.Halt,
                           self.InRadius, self.OutRadius, self.Movement, self.OTATime, self.OTAIP, self.OTAPort)

    def from_dict(self, input_dict: dict):
        self.Result = input_dict['Result']
        self.Schedule = input_dict['Schedule']
        self.RouteID = input_dict['RouteID']
        self.RouteDirect = input_dict['RouteDirect']
        self.RouteBranch = input_dict['RouteBranch']
        self.RouteVer = input_dict['RouteVer']
        self.Reserved = input_dict['Reserved']
        self.DriverID = input_dict['DriverID']
        self.DriverName = input_dict['DriverName']
        self.DepartHr = input_dict['DepartHr']
        self.DepartMin = input_dict['DepartMin']
        self.Year = input_dict['Year']
        self.Month = input_dict['Month']
        self.Day = input_dict['Day']
        self.Hour = input_dict['Hour']
        self.Min = input_dict['Min']
        self.Sec = input_dict['Sec']
        self.Event = input_dict['Event']
        self.RPM = input_dict['RPM']
        self.Accelerate = input_dict['Accelerate']
        self.Decelerate = input_dict['Decelerate']
        self.Halt = input_dict['Halt']
        self.InRadius = input_dict['InRadius']
        self.OutRadius = input_dict['OutRadius']
        self.Movement = input_dict['Movement']
        self.OTATime = input_dict['OTATime']
        self.OTAIP = input_dict['OTAIP']
        self.OTAPort = input_dict['OTAPort']

        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'Result': self.Result,
            'Schedule': self.Schedule,
            'RouteID': self.RouteID,
            'RouteDirect': self.RouteDirect,
            'RouteBranch': self.RouteBranch,
            'RouteVer': self.RouteVer,
            'Reserved': self.Reserved,
            'DriverID': self.DriverID,
            'DriverName': self.DriverName,
            'DepartHr': self.DepartHr,
            'DepartMin': self.DepartMin,
            'Year': self.Year,
            'Month': self.Month,
            'Day': self.Day,
            'Hour': self.Hour,
            'Min': self.Min,
            'Sec': self.Sec,
            'Event': self.Event,
            'RPM': self.RPM,
            'Accelerate': self.Accelerate,
            'Decelerate': self.Decelerate,
            'Halt': self.Halt,
            'InRadius': self.InRadius,
            'OutRadius': self.OutRadius,
            'Movement': self.Movement,
            'OTATime': self.OTATime,
            'OTAIP': self.OTAIP,
            'OTAPort': self.OTAPort
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
