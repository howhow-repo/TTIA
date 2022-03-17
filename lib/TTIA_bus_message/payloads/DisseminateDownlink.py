import struct
from ..message_base import MessageBase


class DisseminateContent(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.MsgIndex = 0
        self.MsgLen = 0
        self.MsgContent = ''
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<BB', pdu)
        self.MsgIndex = payload[0]
        self.MsgLen = payload[1]

        pdu = pdu[2:2+self.MsgLen]
        self.MsgContent = pdu.decode('big5').rstrip('\x00')

        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        MsgContent = bytearray(self.MsgContent.encode("big5"))
        self.MsgLen = len(MsgContent)
        return struct.pack('<BB', self.MsgIndex, self.MsgLen) + MsgContent

    def from_dict(self, input_dict: dict):
        self.MsgIndex = input_dict['MsgIndex']
        self.MsgLen = input_dict['MsgLen']
        self.MsgContent = input_dict['MsgContent']
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'MsgIndex': self.MsgIndex,
            'MsgLen': self.MsgLen,
            'MsgContent': self.MsgContent,
        }
        return r

    def from_default(self):
        pass


class DisseminateDownlink(MessageBase):
    MessageID = 0xE0

    def __init__(self, init_data, init_type: str):
        self.MsgNum = 0
        self.DisseminateContent = []
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MsgNum = struct.unpack('B', pdu[0])[0]
        pdu = pdu[1:]
        for i in range(self.MsgNum):
            content_len = pdu[1]+2
            self.DisseminateContent.append(DisseminateContent(pdu[:content_len], 'pdu'))
            pdu = pdu[content_len:]

    def to_pdu(self) -> bytes:
        self.MsgNum = len(self.DisseminateContent)
        head = struct.pack('B', self.MsgNum)
        Content = bytes()
        for content in self.DisseminateContent:
            Content += content.to_pdu()

        return head + Content

    def from_dict(self, input_dict: dict):
        self.MsgNum = input_dict['MsgNum']
        self.DisseminateContent = [DisseminateContent(content, 'dict') for content in input_dict['DisseminateContent']]
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'MsgNum': self.MsgNum,
            'DisseminateContent': [content.to_dict() for content in self.DisseminateContent],
        }
        return r

    def from_default(self):
        pass
