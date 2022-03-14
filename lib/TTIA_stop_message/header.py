import struct

from .message_base import MessageBase, MessageConstants


class Header(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.ProtocolID = MessageConstants.ProtocolID
        self.ProtocolVer = MessageConstants.ProtocolVer
        self.MessageID = 0
        self.Provider = 0
        self.StopID = 0
        self.Sequence = 0
        self.Len = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, header_pdu, offset=0):
        header = struct.unpack('<4sBBHQHH', header_pdu)
        self.ProtocolID = header[0].decode()
        self.ProtocolVer = header[1]
        self.MessageID = header[2]
        self.Provider = header[3]
        self.StopID = header[4]
        self.Sequence = header[5]
        self.Len = header[6]

    def to_pdu(self):
        byte_like_ProtocolID = str.encode(self.ProtocolID)
        return struct.pack('<4sBBHQHH', byte_like_ProtocolID, self.ProtocolVer, self.MessageID,
                           self.Provider, self.StopID, self.Sequence, self.Len)

    def from_dict(self, input_dict):
        self.ProtocolID = input_dict['ProtocolID']
        self.ProtocolVer = input_dict['ProtocolVer']
        self.MessageID = input_dict['MessageID']
        self.Provider = input_dict['Provider']
        self.StopID = input_dict['StopID']
        self.Sequence = input_dict['Sequence']
        self.Len = input_dict['Len']

    def to_dict(self):
        r = {
            'ProtocolID': self.ProtocolID,
            'ProtocolVer': self.ProtocolVer,
            'MessageID': self.MessageID,
            'Provider': self.Provider,
            'StopID': self.StopID,
            'Sequence': self.Sequence,
            'Len': self.Len,
        }
        return r

    def from_default(self):
        pass
