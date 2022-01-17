import struct

from .message_base import MessageBase


class TimeStruct(MessageBase):
    def from_pdu(self, pdu, offset=0):
        header = struct.unpack_from('<BBBBBB', pdu, offset)
        self.Year = 2000 + header[0]
        self.Month = header[1]
        self.Day = header[2]
        self.Hour = header[3]
        self.Minute = header[4]
        self.Second = header[5]

    def to_pdu(self):
        return struct.pack('<BBBBBB', self.Year - 2000, self.Month, self.Day, self.Hour, self.Minute, self.Second)
