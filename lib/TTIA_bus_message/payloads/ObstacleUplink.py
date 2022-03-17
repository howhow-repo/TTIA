import struct
from ..message_base import MessageBase


class ObstacleUplink(MessageBase):
    MessageID = 0xF0

    def __init__(self, init_data, init_type: str):
        self.Module = 0
        self.Code = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<BB', pdu)
        self.Module = payload[0]
        self.Code = payload[1]

        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()

        return struct.pack('<BB', self.Module, self.Code)

    def from_dict(self, input_dict: dict):
        self.Module = input_dict['Module']
        self.Code = input_dict['Code']

        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'Module': self.Module,
            'Code': self.Code,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass


class ModuleCode:
    GPS = 0x01
    LCD = 0x02
    LED = 0x03
    DCR = 0x04
    ETM = 0x05
    ADA = 0x06
