import struct
from .payload_base import PayloadBase


class ReportSetBrightnessDownlink(PayloadBase):
    message_id = 0x0D
    message_cname = "亮度設定"

    def __init__(self, init_data, init_type):
        self.LightSet = 15
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<B', pdu)
        self.LightSet = payload[0]
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        return struct.pack('<B', self.LightSet)

    def from_dict(self, input_dict: dict):
        self.LightSet = input_dict['LightSet']
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'LightSet': self.LightSet,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        assert 0 <= self.LightSet <= 15, "LightSet should be 0~15; 0:min 15:max"
