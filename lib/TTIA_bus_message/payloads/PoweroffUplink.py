import struct
from ..message_base import MessageBase
from ..tables import MonitorStructType2


class PoweroffUplink(MessageBase):
    MessageID = 0x0A

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.PSDReconnect = 0
        self.PacketRatio = 0
        self.GPSRatio = 100

        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<HBB', pdu[30:])
        self.PSDReconnect = payload[0]
        self.PacketRatio = payload[1]
        self.GPSRatio = payload[2]

        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        bMonitorData = self.MonitorData.to_pdu()

        return bMonitorData + struct.pack('<HBB', self.PSDReconnect, self.PacketRatio, self.GPSRatio)

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.PSDReconnect = input_dict['PSDReconnect']
        self.PacketRatio = input_dict['PacketRatio']
        self.GPSRatio = input_dict['GPSRatio']

        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'PSDReconnect': self.PSDReconnect,
            'PacketRatio': self.PacketRatio,
            'GPSRatio': self.GPSRatio,
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
