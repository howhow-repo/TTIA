import struct
from ..message_base import MessageBase


class RouteUplink(MessageBase):
    MessageID = 0x02

    def __init__(self, init_data, init_type: str):
        self.RouteID = 0
        self.RouteDirect = 0
        self.RouteBranch = ''
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<HB1s', pdu)
        self.RouteID = payload[0]
        self.RouteDirect = payload[1]
        self.RouteBranch = payload[2].decode().rstrip('\0')
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        RouteBranch = str.encode(self.RouteBranch)
        return struct.pack('<HB1s', self.RouteID, self.RouteDirect, RouteBranch)

    def from_dict(self, input_dict: dict):
        self.RouteID = input_dict['RouteID']
        self.RouteDirect = input_dict['RouteDirect']
        self.RouteBranch = input_dict['RouteBranch']
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'RouteID': self.RouteID,
            'RouteDirect': self.RouteDirect,
            'RouteBranch': self.RouteBranch
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
