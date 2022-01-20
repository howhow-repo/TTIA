import struct
from .payload_base import PayloadBase


class ReportUpdateGifDownlink(PayloadBase):
    message_id = 0x12

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HH160s160s', pdu)
        self.PicNo = payload[0]
        self.PicNum = payload[1]
        self.PicURL = bytearray(payload[2]).decode('ascii').rstrip('\x00')
        self.MsgContent = bytearray(payload[3]).decode('big5').rstrip('\x00')

    def to_pdu(self):
        return struct.pack("<HH160s160s", self.PicNo, self.PicNum,
                           bytearray(self.PicURL.encode('ascii')),
                           bytearray(self.MsgContent.encode('big5'))
                           )

    def from_dict(self, json):
        self.PicNo = json['PicNo']
        self.PicNum = json['PicNum']
        self.PicURL = json['PicURL']
        self.MsgContent = json['MsgContent']

    def to_dict(self):
        r = {
            'PicNo': self.PicNo,
            'PicNum': self.PicNum,
            'PicURL': self.PicURL,
            'MsgContent': self.MsgContent,
        }
        return r

    def from_default(self):
        self.PicNo = 0
        self.PicNum = 0
        self.PicURL = ''
        self.MsgContent = ''
