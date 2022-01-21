import struct
from .op_payload_base import OpPayloadBase


class OpEmpty(OpPayloadBase):
    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        pass

    def to_pdu(self):
        return b''

    def from_dict(self, input_dict):
        pass

    def to_dict(self):
        return {}

    def from_default(self):
        pass