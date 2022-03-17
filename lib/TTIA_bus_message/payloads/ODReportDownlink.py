from ..message_base import MessageBase


class ODReportDownlink(MessageBase):
    MessageID = 0xF3

    def __init__(self, init_data, init_type: str):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        pass

    def to_pdu(self) -> bytes:
        pass

    def from_dict(self, input_dict: dict):
        pass

    def to_dict(self) -> dict:
        return {}

    def from_default(self):
        pass
