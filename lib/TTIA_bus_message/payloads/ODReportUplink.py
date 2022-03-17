import struct
from ..tables.ODStruct import ODStruct
from ..message_base import MessageBase


class ODReportUplink(MessageBase):
    MessageID = 0xF2

    def __init__(self, init_data, init_type: str):
        self.RouteID = 0
        self.RouteDirect = 0
        self.RouteBranch = ''
        self.ODRecord_No = 0
        self.Reserved = 0
        self.ODRecord = []
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<HBBBB', pdu[:6])
        self.RouteID = payload[0]
        self.RouteDirect = payload[1]
        self.RouteBranch = payload[2]
        self.ODRecord_No = payload[3]
        self.Reserved = payload[4]

        pdu = pdu[6:]
        for i in range(self.ODRecord_No):
            OD_len = 15 + pdu[14]*2
            self.ODRecord.append(ODStruct(pdu[:OD_len], 'pdu'))
            pdu = pdu[OD_len:]

        self.self_assert()

    def to_pdu(self) -> bytes:
        head = struct.pack('<HBBBB', self.RouteID, self.RouteDirect, self.RouteBranch, self.ODRecord_No, self.Reserved)
        Records = bytes()
        for record in self.ODRecord:
            Records += record.to_pdu()
        return head + Records

    def from_dict(self, input_dict: dict):
        self.RouteID = input_dict['RouteID']
        self.RouteDirect = input_dict['RouteDirect']
        self.RouteBranch = input_dict['RouteBranch']
        self.ODRecord_No = input_dict['ODRecord_No']
        self.Reserved = input_dict['Reserved']
        self.ODRecord = [ODStruct(record, 'dict') for record in input_dict['ODRecord']]

        self.self_assert()

    def to_dict(self) -> dict:
        r = {
            'RouteID': self.RouteID,
            'RouteDirect': self.RouteDirect,
            'RouteBranch': self.RouteBranch,
            'ODRecord_No': self.ODRecord_No,
            'Reserved': self.Reserved,
            'ODRecord': [record.to_dict() for record in self.ODRecord],
        }
        return r

    def from_default(self):
        pass
