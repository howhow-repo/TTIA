import struct

from .message_base import MessageBase, MessageConstants


class Header(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.ProtocolID = MessageConstants.ProtocolID
        self.ProtocolVer = MessageConstants.ProtocolVer
        self.MessageID = 0
        self.CustomerID = MessageConstants.CustomerID
        self.CarID = 0
        self.IDStorage = 0
        self.DriverID = 0
        self.Sequence = 0
        self.Reserved = 0
        self.Len = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, header_pdu, offset=0):
        header = struct.unpack('<4sBBHHBIHBH', header_pdu)
        self.ProtocolID = header[0]
        self.ProtocolVer = header[1]
        self.MessageID = header[2]
        self.CustomerID = header[3]
        self.CarID = header[4]
        self.IDStorage = header[5]
        self.DriverID = header[6]
        self.Sequence = header[7]
        self.Reserved = header[8]
        self.Len = header[9]
        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        byte_like_ProtocolID = str.encode(self.ProtocolID)
        return struct.pack('<4sBBHHBIHBH', byte_like_ProtocolID, self.ProtocolVer, self.MessageID, self.CustomerID,
                           self.CarID, self.IDStorage, self.DriverID, self.Sequence, self.Reserved, self.Len)

    def from_dict(self, input_dict):
        self.ProtocolID = input_dict['ProtocolID']
        self.ProtocolVer = input_dict['ProtocolVer']
        self.MessageID = input_dict['MessageID']
        self.CustomerID = input_dict['CustomerID']
        self.CarID = input_dict['CarID']
        self.IDStorage = input_dict['IDStorage']
        self.DriverID = input_dict['DriverID']
        self.Sequence = input_dict['Sequence']
        self.Reserved = input_dict['Reserved']
        self.Len = input_dict['Len']
        self.self_assert()

    def to_dict(self):
        self.self_assert()
        r = {
            'ProtocolID': self.ProtocolID,
            'ProtocolVer': self.ProtocolVer,
            'MessageID': self.MessageID,
            'CustomerID': self.CustomerID,
            'CarID': self.CarID,
            'IDStorage': self.IDStorage,
            'DriverID': self.DriverID,
            'Sequence': self.Sequence,
            'Reserved': self.Reserved,
            'Len': self.Len,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
