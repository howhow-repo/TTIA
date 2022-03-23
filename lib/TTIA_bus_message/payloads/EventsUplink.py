import struct
from ..message_base import MessageBase
from ..tables.EventCode import EventCode


class EventsUplink(MessageBase):
    MessageID = 0x08

    def __init__(self, init_data, init_type: str):
        self.EventType = 1
        self.RouteID = 0
        self.RouteDirect = 0
        self.RouteBranch = ''
        self.EventContent = EventCode.get_default_content(self.EventType)
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<HHB1s', pdu)
        self.EventType = payload[0]
        self.RouteID = payload[1]
        self.RouteDirect = payload[2]
        self.RouteBranch = payload[3].decode().rstrip('\0')
        self.EventContent = EventCode.get_default_content(self.EventType)
        self.EventContent.from_pdu(pdu[6:])

        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        head = struct.pack('<HHB1s', self.EventType, self.RouteID, self.RouteDirect, self.RouteBranch.encode())
        EventContent = self.EventContent.to_pdu()

        return head + EventContent

    def from_dict(self, input_dict: dict):
        self.EventType = input_dict['EventType']
        self.RouteID = input_dict['RouteID']
        self.RouteDirect = input_dict['RouteDirect']
        self.RouteBranch = input_dict['RouteBranch']
        self.EventContent = EventCode.get_default_content(self.EventType)
        self.EventContent.from_dict(input_dict['EventContent'])

        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'EventType': self.EventType,
            'RouteID': self.RouteID,
            'RouteDirect': self.RouteDirect,
            'RouteBranch': self.RouteBranch,
            'EventContent': self.EventContent.to_dict()
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
