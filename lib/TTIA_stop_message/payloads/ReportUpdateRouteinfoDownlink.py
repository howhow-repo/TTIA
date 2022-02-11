import struct
from .payload_base import PayloadBase


class ReportUpdateRouteinfoDownlink(PayloadBase):
    message_id = 0x0B
    message_cname = "路線資料設定訊息"

    def __init__(self, init_data, init_type):
        self.RouteID = 0
        self.PathCName = ''
        self.PathEName = ''
        self.Sequence = 0
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<H12s12sH', pdu)
        self.RouteID = payload[0]
        self.PathCName = payload[1].decode('big5').rstrip('\x00')
        self.PathEName = payload[2].decode('ascii').rstrip('\x00')
        self.Sequence = payload[3]
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        PathCName = bytearray(self.PathCName.encode('big5'))
        PathEName = bytearray(self.PathEName.encode('ascii'))
        return struct.pack('<H12s12sH', self.RouteID, PathCName, PathEName, self.Sequence)

    def from_dict(self, input_dict: dict):
        self.RouteID = input_dict['RouteID']
        self.PathCName = input_dict['PathCName']
        self.PathEName = input_dict['PathEName']
        self.Sequence = input_dict['Sequence']
        self.self_assert()

    def to_dict(self) -> dict:
        r = {
            'RouteID': self.RouteID,
            'PathCName': self.PathCName,
            'PathEName': self.PathEName,
            'Sequence': self.Sequence,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        PathCName = bytearray(self.PathCName.encode('big5'))
        assert len(PathCName) <= 12, "PathCName overflow, please make sure it beneath 12 bytes"
        PathEName = bytearray(self.PathEName.encode('ascii'))
        assert len(PathEName) <= 12, "PathEName overflow, please make sure it beneath 12 bytes"
        assert 0 <= self.RouteID <= 65535, "RouteID overflow, format requires 0 <= number <= 65535"
