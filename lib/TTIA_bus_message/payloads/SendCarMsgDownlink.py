import struct
from ..message_base import MessageBase


class SendCarMsgDownlink(MessageBase):
    MessageID = 0x06

    def __init__(self, init_data, init_type: str):
        self.Action = 0
        self.InfoID = 0
        self.Reserved = 0
        self.Information = ''
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<HB', pdu[:3])
        self.Action = payload[0]
        self.InfoID = payload[1]
        self.Information = pdu[3:].decode('big5', "ignore").rstrip('\x00')
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        head = struct.pack('<HB', self.Action, self.InfoID)
        Information = self.Information.encode('big5')
        return head + Information

    def from_dict(self, input_dict: dict):
        self.Action = input_dict['Action']
        self.InfoID = input_dict['InfoID']
        self.Information = input_dict['Information']
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'Action': self.Action,
            'InfoID': self.InfoID,
            'Information': self.Information,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
