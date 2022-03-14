import struct
from ..message_base import MessageBase


class TimeStruct(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.Year = 2000
        self.Month = 1
        self.Day = 1
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        pdu = struct.unpack('<6B', pdu)
        self.Year = pdu[0] + 2000
        self.Month = pdu[1]
        self.Day = pdu[2]
        self.Hour = pdu[3]
        self.Minute = pdu[4]
        self.Second = pdu[5]

        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        return struct.pack('<6B',
                           self.Year - 2000, self.Month, self.Day,
                           self.Hour, self.Minute, self.Second)

    def from_dict(self, input_dict: dict):
        self.Year = input_dict['Year']
        self.Month = input_dict['Month']
        self.Day = input_dict['Day']
        self.Hour = input_dict['Hour']
        self.Minute = input_dict['Minute']
        self.Second = input_dict['Second']

        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
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
        assert 2000 <= self.Year, f"value: {self.Year}: Year must > 2000"
        assert 1 <= self.Month <= 12, f"value: {self.Month}: Month range error."
        assert 1 <= self.Day <= 31, f"value: {self.Day}: Day range error"
        assert 0 <= self.Hour <= 23, f"value: {self.Hour}: Hour range error"
        assert 0 <= self.Minute <= 59, f"value: {self.Minute}: Min range error"
        assert 0 <= self.Second <= 59, f"value: {self.Second}: Sec range error"
