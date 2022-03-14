import struct
from ..message_base import MessageBase
from ..tables.MonitorStruct import MonitorStructType1


class MonitorUplink(MessageBase):
    MessageID = 0x04

    def __init__(self, init_data, init_type: str):
        self.MonitorData_No = 0
        self.Reserved = 0
        self.MonitorData = []
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<BB', pdu)
        self.MonitorData_No = payload[0]
        self.Reserved = payload[1]
        pdu = pdu[2:]
        data_len = 110
        for i in range(self.MonitorData_No):
            Data = MonitorStructType1(pdu[data_len * i:(data_len * i) + data_len], 'pdu')
            self.MonitorData.append(Data)
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        head = struct.pack('<BB', self.MonitorData_No, self.Reserved)
        bData = bytes()
        for data in self.MonitorData:
            bData += data.to_pdu()

        return head + bData

    def from_dict(self, input_dict: dict):
        self.MonitorData_No = input_dict['MonitorData_No']
        self.Reserved = input_dict['Reserved']
        self.MonitorData = [MonitorStructType1(data, 'dict') for data in input_dict['MonitorData']]
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'MonitorData_No': self.MonitorData_No,
            'Reserved': self.Reserved,
            'MonitorData': [data.to_dict() for data in self.MonitorData]
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
