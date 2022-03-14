import struct
from ..message_base import MessageBase
from .TimeStruct import TimeStruct


class ODStruct(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.OrgStopID = 0
        self.DstStopID = 0
        self.OrgODTime = TimeStruct({}, 'default')
        self.DstODTime = TimeStruct({}, 'default')
        self.RemainingNum = 0
        self.RecordNum = 0
        self.TypeID1 = 0
        self.TypeNum1 = 0
        self.TypeIDN = 0
        self.TypeNumN = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.OrgStopID = pdu[0]
        self.DstStopID = pdu[1]
        self.OrgODTime = TimeStruct(pdu[2:2 + 6], 'pdu')
        self.DstODTime = TimeStruct(pdu[2 + 6:2 + 6 + 6], 'pdu')
        pdu = struct.unpack('<BBBBBB', pdu[14:])
        self.RemainingNum = pdu[0]
        self.RecordNum = pdu[1]
        self.TypeID1 = pdu[2]
        self.TypeNum1 = pdu[3]
        self.TypeIDN = pdu[4]
        self.TypeNumN = pdu[5]

    def to_pdu(self) -> bytes:
        OrgStopID = struct.pack('<B', self.OrgStopID)
        DstStopID = struct.pack('<B', self.DstStopID)
        OrgODTime = self.OrgODTime.to_pdu()
        DstODTime = self.DstODTime.to_pdu()
        return OrgStopID \
               + DstStopID \
               + OrgODTime \
               + DstODTime \
               + struct.pack('<BBBBBB',
                             self.RemainingNum, self.RecordNum, self.TypeID1,
                             self.TypeNum1, self.TypeIDN, self.TypeNumN)

    def from_dict(self, input_dict: dict):
        self.OrgStopID = input_dict['OrgStopID']
        self.DstStopID = input_dict['DstStopID']
        self.OrgODTime = TimeStruct(input_dict['OrgODTime'], 'dict')
        self.DstODTime = TimeStruct(input_dict['DstODTime'], 'dict')
        self.RemainingNum = input_dict['RemainingNum']
        self.RecordNum = input_dict['RecordNum']
        self.TypeID1 = input_dict['TypeID1']
        self.TypeNum1 = input_dict['TypeNum1']
        self.TypeIDN = input_dict['TypeIDN']
        self.TypeNumN = input_dict['TypeNumN']

    def to_dict(self) -> dict:
        r = {
            'OrgStopID': self.OrgStopID,
            'DstStopID': self.DstStopID,
            'OrgODTime': self.OrgODTime.to_dict(),
            'DstODTime': self.DstODTime.to_dict(),
            'RemainingNum': self.RemainingNum,
            'RecordNum': self.RecordNum,
            'TypeID1': self.TypeID1,
            'TypeNum1': self.TypeNum1,
            'TypeIDN': self.TypeIDN,
            'TypeNumN': self.TypeNumN
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
