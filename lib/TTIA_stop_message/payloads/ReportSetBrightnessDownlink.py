import struct
from .payload_base import PayloadBase


class ReportSetBrightnessDownlink(PayloadBase):
    message_id = 0x0D

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<B', pdu)
        self.LightSet = payload[0]

    def to_pdu(self):
        return struct.pack('<B', self.LightSet)

    def from_dict(self, json):
        self.LightSet = json['LightSet']

    def to_dict(self):
        r = {
            'LightSet': self.LightSet,
        }
        return r

    def from_default(self):
        self.LightSet = 15
