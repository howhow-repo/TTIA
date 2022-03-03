from .payload_base import PayloadBase


class ReportMsgcountDownlink(PayloadBase):
    message_id = 0x04
    message_cname = "定時回報確認訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        pass

    def to_pdu(self) -> bytes:
        return b''

    def from_dict(self, input_dict: dict):
        pass

    def to_dict(self) -> dict:
        r = {}
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
