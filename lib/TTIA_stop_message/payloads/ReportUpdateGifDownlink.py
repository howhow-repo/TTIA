import struct
from .payload_base import PayloadBase


class ReportUpdateGifDownlink(PayloadBase):
    message_id = 0x12
    message_cname = "動態圖示通知訊息"

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HH160s160s', pdu)
        self.PicNo = payload[0]
        self.PicNum = payload[1]
        self.PicURL = bytearray(payload[2]).decode('ascii').rstrip('\x00')
        self.MsgContent = bytearray(payload[3]).decode('big5').rstrip('\x00')
        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        assert len(bytearray(self.PicURL.encode('ascii'))) <= 160, \
            "PicURL overflow, please make sure it beneath 160 bytes"
        assert len(bytearray(self.MsgContent.encode('big5'))) <= 160, \
            "MsgContent overflow, please make sure it beneath 160 bytes"
        return struct.pack("<HH160s160s", self.PicNo, self.PicNum,
                           bytearray(self.PicURL.encode('ascii')),
                           bytearray(self.MsgContent.encode('big5'))
                           )

    def from_dict(self, input_dict):
        self.PicNo = input_dict['PicNo']
        self.PicNum = input_dict['PicNum']
        self.PicURL = input_dict['PicURL']
        self.MsgContent = input_dict['MsgContent']
        self.self_assert()

    def to_dict(self):
        self.self_assert()
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

    def self_assert(self):
        pass
