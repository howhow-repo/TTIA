import struct

from ..message_base import MessageBase
from .GPSStruct import GPSStruct


class MonitorStructType1(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.GPSData = GPSStruct({}, 'default')
        self.AvgSpeed = 0
        self.IntSpeed = [0] * 20
        self.RPM = [0] * 20
        self.DutyStatus = 0
        self.BusStatus = 0
        self.Mileage = 0

        super().__init__(init_data, init_type)

    def from_pdu(self, payload: bytes):
        self.GPSData = GPSStruct(payload[:22], 'pdu')
        payload = struct.unpack('<H20H20HBBI', payload[22:])
        self.AvgSpeed = payload[0]
        self.IntSpeed = list(payload[1:21])
        self.RPM = list(payload[21:41])
        self.DutyStatus = payload[41]
        self.BusStatus = payload[42]
        self.Mileage = payload[43]

        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        GPSDataPDU = self.GPSData.to_pdu()
        AvgSpeed = struct.pack('<H', self.AvgSpeed)

        IntSpeed = bytes()
        RPM = bytes()
        for speed in self.IntSpeed:
            IntSpeed += struct.pack('<H', speed)
        for R in self.RPM:
            RPM += struct.pack('<H', R)

        return GPSDataPDU + AvgSpeed + IntSpeed + RPM + struct.pack('<BBI', self.DutyStatus, self.BusStatus, self.Mileage)

    def from_dict(self, input_dict: dict):
        self.GPSData = GPSStruct(input_dict['GPSData'], 'dict')
        self.AvgSpeed = input_dict['AvgSpeed']
        self.IntSpeed = input_dict['IntSpeed']
        self.RPM = input_dict['RPM']
        self.DutyStatus = input_dict['DutyStatus']
        self.BusStatus = input_dict['BusStatus']
        self.Mileage = input_dict['Mileage']

        self.self_assert()

    def to_dict(self) -> dict:
        r = {
            'GPSData': self.GPSData.to_dict(),
            'AvgSpeed': self.AvgSpeed,
            'IntSpeed': self.IntSpeed,
            'RPM': self.RPM,
            'DutyStatus': self.DutyStatus,
            'BusStatus': self.BusStatus,
            'Mileage': self.Mileage,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        assert type(self.IntSpeed) == list, 'type of IntSpeed should List'
        assert len(self.IntSpeed) == 20, 'len IntSpeed should be 20'
        assert type(self.RPM) == list, 'type of RPM should List'
        assert len(self.RPM) == 20, 'len RPM should be 20'


class MonitorStructType2(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.GPSData = GPSStruct({}, 'default')
        self.AvgSpeed = 0
        self.DutyStatus = 0
        self.BusStatus = 0
        self.Mileage = 0

        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.GPSData = GPSStruct(pdu[:22], 'pdu')
        pdu = struct.unpack('<HBBI', pdu[22:])
        self.AvgSpeed = pdu[0]
        self.DutyStatus = pdu[1]
        self.BusStatus = pdu[2]
        self.Mileage = pdu[3]

        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        GPSDataPDU = self.GPSData.to_pdu()
        temp_pdu = struct.pack('<HBBI', self.AvgSpeed, self.DutyStatus, self.BusStatus, self.Mileage)

        return GPSDataPDU + temp_pdu

    def from_dict(self, input_dict: dict):
        self.GPSData = GPSStruct(input_dict['GPSData'], 'dict')
        self.AvgSpeed = input_dict['AvgSpeed']
        self.DutyStatus = input_dict['DutyStatus']
        self.BusStatus = input_dict['BusStatus']
        self.Mileage = input_dict['Mileage']

        self.self_assert()

    def to_dict(self) -> dict:
        r = {
            'GPSData': self.GPSData.to_dict(),
            'AvgSpeed': self.AvgSpeed,
            'DutyStatus': self.DutyStatus,
            'BusStatus': self.BusStatus,
            'Mileage': self.Mileage,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
