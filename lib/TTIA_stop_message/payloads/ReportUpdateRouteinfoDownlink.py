import struct
from .payload_base import PayloadBase


class ReportUpdateRouteinfoDownlink(PayloadBase):
    message_id = 0x0B

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<H12s12sH', pdu)
        self.RouteID = payload[0]
        self.PathCName = bytearray(payload[1]).decode('big5')
        self.PathEName = bytearray(payload[2]).decode('ascii')
        self.Sequence = payload[3]

    def to_pdu(self):
        return struct.pack('<H12s12sH', self.RouteID,
                           bytearray(self.PathCName.encode('big5')),
                           bytearray(self.PathEName.encode('ascii')),
                           self.Sequence
                           )

    def from_dict(self, json):
        self.RouteID = json['RouteID']
        self.PathCName = json['PathCName']
        self.PathEName = json['PathEName']
        self.Sequence = json['Sequence']

    def to_dict(self):
        r = {
            'RouteID': self.RouteID,
            'PathCName': self.PathCName,
            'PathEName': self.PathEName,
            'Sequence': self.Sequence,
        }
        return r

    def from_default(self):
        self.RouteID = 0
        self.PathCName = '中文站名'
        self.PathEName = 'stop eng name'
        self.Sequence = 0
