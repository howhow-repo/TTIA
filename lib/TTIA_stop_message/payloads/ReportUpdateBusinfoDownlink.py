import struct

from .payload_base import PayloadBase


class ReportUpdateBusinfoDownlink(PayloadBase):
    message_id = 0x07
    message_cname = "更新即時公車資訊訊息"

    def __init__(self, init_data, init_type):
        self.from_default()
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HHQQBHHBBBBBBBBBBBBBBB', pdu)
        self.RouteID = payload[0]
        self.BusID = payload[1]
        self.CurrentStop = payload[2]
        self.DestinationStop = payload[3]
        self.IsLastBus = payload[4]
        self.EstimateTime = payload[5]
        self.StopDistance = payload[6]
        self.Direction = payload[7]
        self.Type = payload[8]
        self.TransYear = payload[9] + 2000
        self.TransMonth = payload[10]
        self.TransDay = payload[11]
        self.TransHour = payload[12]
        self.TransMinute  = payload[13]
        self.TransSecond = payload[14]
        self.RcvYear = payload[15] + 2000
        self.RcvMonth = payload[16]
        self.RcvDay = payload[17]
        self.RcvHour = payload[18]
        self.RcvMinute = payload[19]
        self.RcvSecond = payload[20]
        self.Reserved = payload[21]

    def to_pdu(self):
        return struct.pack('<HHQQBHHBBBBBBBBBBBBBBB', self.RouteID, self.BusID, self.CurrentStop,
                           self.DestinationStop, self.IsLastBus, self.EstimateTime, self.StopDistance,
                           self.Direction,
                           self.Type, self.TransYear - 2000, self.TransMonth, self.TransDay, self.TransHour,
                           self.TransMinute, self.TransSecond,
                           self.RcvYear - 2000, self.RcvMonth, self.RcvDay, self.RcvHour, self.RcvMinute,
                           self.RcvSecond, self.Reserved,)

    def from_dict(self, input_dict):
        self.RouteID = input_dict['RouteID']
        self.BusID = input_dict['BusID']
        self.CurrentStop = input_dict['CurrentStop']
        self.DestinationStop = input_dict['DestinationStop']
        self.IsLastBus = input_dict['IsLastBus']
        self.EstimateTime = input_dict['EstimateTime']
        self.StopDistance = input_dict['StopDistance']
        self.Direction = input_dict['Direction']
        self.Type = input_dict['Type']
        self.TransYear = input_dict['TransYear']
        self.TransMonth = input_dict['TransMonth']
        self.TransDay = input_dict['TransDay']
        self.TransHour = input_dict['TransHour']
        self.TransMinute = input_dict['TransMinute']
        self.TransSecond = input_dict['TransSecond']
        self.RcvYear = input_dict['RcvYear']
        self.RcvMonth = input_dict['RcvMonth']
        self.RcvDay = input_dict['RcvDay']
        self.RcvHour = input_dict['RcvHour']
        self.RcvMinute = input_dict['RcvMinute']
        self.RcvSecond = input_dict['RcvSecond']
        self.Reserved = input_dict['Reserved']

    def to_dict(self):
        r = {
            'RouteID': self.RouteID,
            'BusID': self.BusID,
            'CurrentStop': self.CurrentStop,
            'DestinationStop': self.DestinationStop,
            'IsLastBus': self.IsLastBus,
            'EstimateTime': self.EstimateTime,
            'StopDistance': self.StopDistance,
            'Direction': self.Direction,
            'Type': self.Type,
            'TransYear': self.TransYear,
            'TransMonth': self.TransMonth,
            'TransDay': self.TransDay,
            'TransHour': self.TransHour,
            'TransMinute': self.TransMinute,
            'TransSecond': self.TransSecond,
            'RcvYear': self.RcvYear,
            'RcvMonth': self.RcvMonth,
            'RcvDay': self.RcvDay,
            'RcvHour': self.RcvHour,
            'RcvMinute': self.RcvMinute,
            'RcvSecond': self.RcvSecond,
            'Reserved': self.Reserved,
        }
        return r

    def from_default(self):
        self.RouteID = 0
        self.BusID = 0
        self.CurrentStop = 0
        self.DestinationStop = 0
        self.IsLastBus = 0
        self.EstimateTime = 0
        self.StopDistance = 0
        self.Direction = 0
        self.Type = 0
        self.TransYear = 2000
        self.TransMonth = 1
        self.TransDay = 1
        self.TransHour = 0
        self.TransMinute = 0
        self.TransSecond = 0
        self.RcvYear = 2000
        self.RcvMonth = 1
        self.RcvDay = 1
        self.RcvHour = 0
        self.RcvMinute = 0
        self.RcvSecond = 0
        self.Reserved = 0
        self.min = 0


