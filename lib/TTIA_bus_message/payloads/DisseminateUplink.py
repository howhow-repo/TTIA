from ..message_base import MessageBase


class DisseminateUplink(MessageBase):
    MessageID = 0xE1

    def __init__(self, init_data, init_type: str):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        pass

    def to_pdu(self) -> bytes:
        return b''

    def from_dict(self, input_dict: dict):
        pass

    def to_dict(self) -> dict:
        return {}

    def from_default(self):
        pass