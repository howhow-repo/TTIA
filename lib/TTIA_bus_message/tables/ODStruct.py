import struct
from ..message_base import MessageBase
from .TimeStruct import TimeStruct


class Record(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.TypeID = 0
        self.TypeNum = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        pdu = struct.unpack('<BB', pdu)
        self.TypeID = pdu[0]
        self.TypeNum = pdu[1]

    def to_pdu(self) -> bytes:
        return struct.pack('<BB', self.TypeID, self.TypeNum)

    def from_dict(self, input_dict: dict):
        self.TypeID = input_dict['TypeID']
        self.TypeNum = input_dict['TypeNum']

    def to_dict(self) -> dict:
        r = {
            'TypeID': self.TypeID,
            'TypeNum': self.TypeNum,
        }
        return r

    def from_default(self):
        pass


class ODStruct(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.OrgStopID = 0
        self.DstStopID = 0
        self.OrgODTime = TimeStruct({}, 'default')
        self.DstODTime = TimeStruct({}, 'default')
        self.RemainingNum = 0
        self.RecordNum = 0
        self.Records = []
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.OrgStopID = pdu[0]
        self.DstStopID = pdu[1]
        self.OrgODTime = TimeStruct(pdu[2:8], 'pdu')
        self.DstODTime = TimeStruct(pdu[8:14], 'pdu')

        pdu = struct.unpack('<BB', pdu[14:15])
        self.RemainingNum = pdu[0]
        self.RecordNum = pdu[1]

        pdu = pdu[15:]
        for i in range(self.RecordNum):
            record = Record(pdu[2 * i:(2 * i) + 2], 'pdu')
            self.Records.append(record)

    def to_pdu(self) -> bytes:
        OrgStopID = struct.pack('<B', self.OrgStopID)
        DstStopID = struct.pack('<B', self.DstStopID)
        OrgODTime = self.OrgODTime.to_pdu()
        DstODTime = self.DstODTime.to_pdu()
        head = OrgStopID + DstStopID + OrgODTime + DstODTime
        Records = bytes()
        for data in self.Records:
            Records += data.to_pdu()
        return head + struct.pack('<BB', self.RemainingNum, len(self.Records), ) + Records

    def from_dict(self, input_dict: dict):
        self.OrgStopID = input_dict['OrgStopID']
        self.DstStopID = input_dict['DstStopID']
        self.OrgODTime = TimeStruct(input_dict['OrgODTime'], 'dict')
        self.DstODTime = TimeStruct(input_dict['DstODTime'], 'dict')
        self.RemainingNum = input_dict['RemainingNum']
        self.RecordNum = input_dict['RecordNum']
        self.Records = [Record(record, 'dict') for record in input_dict['Record']]

    def to_dict(self) -> dict:
        r = {
            'OrgStopID': self.OrgStopID,
            'DstStopID': self.DstStopID,
            'OrgODTime': self.OrgODTime.to_dict(),
            'DstODTime': self.DstODTime.to_dict(),
            'RemainingNum': self.RemainingNum,
            'RecordNum': self.RecordNum,
            'Records': [record.to_dict() for record in self.Records],
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
