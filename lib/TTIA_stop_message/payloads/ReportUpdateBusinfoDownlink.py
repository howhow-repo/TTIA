import struct

from .payload_base import PayloadBase


class ReportUpdateBusinfoDownlink(PayloadBase):
    message_id = 0x07
    message_cname = "更新即時公車資訊訊息"

    def __init__(self, init_data, init_type):
        self.RouteID = 0
        self.BusID = 0
        self.CurrentStop = 0
        self.DestinationStop = 0
        self.IsLastBus = 0
        self.EstimateTime = 0
        self.StopDistance = 0
        self.Direction = 0
        self.Type = 1
        self.TransYear = 2000
        self.TransMonth = 1
        self.TransDay = 1
        self.TransHour = 0
        self.TransMin = 0
        self.TransSec = 0
        self.RcvYear = 2000
        self.RcvMonth = 1
        self.RcvDay = 1
        self.RcvHour = 0
        self.RcvMin = 0
        self.RcvSec = 0
        self.Reserved = 0
        self.min = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
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
        self.TransMin  = payload[13]
        self.TransSec = payload[14]
        self.RcvYear = payload[15] + 2000
        self.RcvMonth = payload[16]
        self.RcvDay = payload[17]
        self.RcvHour = payload[18]
        self.RcvMin = payload[19]
        self.RcvSec = payload[20]
        self.Reserved = payload[21]
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        return struct.pack('<HHQQBHHBBBBBBBBBBBBBBB', self.RouteID, self.BusID, self.CurrentStop,
                           self.DestinationStop, self.IsLastBus, self.EstimateTime, self.StopDistance,
                           self.Direction,
                           self.Type, self.TransYear - 2000, self.TransMonth, self.TransDay, self.TransHour,
                           self.TransMin, self.TransSec,
                           self.RcvYear - 2000, self.RcvMonth, self.RcvDay, self.RcvHour, self.RcvMin,
                           self.RcvSec, self.Reserved,)

    def from_dict(self, input_dict: dict):
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
        self.TransMin = input_dict['TransMin']
        self.TransSec = input_dict['TransSec']
        self.RcvYear = input_dict['RcvYear']
        self.RcvMonth = input_dict['RcvMonth']
        self.RcvDay = input_dict['RcvDay']
        self.RcvHour = input_dict['RcvHour']
        self.RcvMin = input_dict['RcvMin']
        self.RcvSec = input_dict['RcvSec']
        self.Reserved = input_dict['Reserved']
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
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
            'TransMin': self.TransMin,
            'TransSec': self.TransSec,
            'RcvYear': self.RcvYear,
            'RcvMonth': self.RcvMonth,
            'RcvDay': self.RcvDay,
            'RcvHour': self.RcvHour,
            'RcvMin': self.RcvMin,
            'RcvSec': self.RcvSec,
            'Reserved': self.Reserved,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        assert self.IsLastBus in [0, 1], "IsLastBus should be 0~1; 0:非末班車 1:末班車"
        assert self.Direction in range(0, 4), "Direction should be 0~3; 0:去程 1:返程 2:尚未發車 3:末班已離駛"
        assert self.Type in [1, 2], "Type should be 1~2; 1:定期 2:非定期"
        assert 2000 <= self.TransYear, "TransYear must > 2000"
        assert 1 <= self.TransMonth <= 12, "TransMonth range error"
        assert 1 <= self.TransDay <= 31, "TransDay range error"
        assert 0 <= self.TransHour <= 23, "TransHour range error"
        assert 0 <= self.TransMin <= 59, "TransMin range error"
        assert 0 <= self.TransSec <= 59, "TransSec range error"
        assert 2000 <= self.RcvYear, "RcvYear must > 2000"
        assert 1 <= self.RcvMonth <= 12, "RcvMonth range error"
        assert 1 <= self.RcvDay <= 31, "RcvDay range error"
        assert 0 <= self.RcvHour <= 59, "RcvHour range error"
        assert 0 <= self.RcvMin <= 59, "RcvMin range error"
        assert 0 <= self.RcvSec <= 59, "RcvSec range error"
