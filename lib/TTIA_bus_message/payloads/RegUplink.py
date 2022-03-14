import struct
from ..message_base import MessageBase
from ..tables import MonitorStructType2
from ..tables import FileStruct


class RegUplink(MessageBase):
    MessageID = 0x00

    def __init__(self, init_data, init_type: str):
        self.MonitorData = MonitorStructType2({}, 'default')
        self.IMSI = ''
        self.IMEI = ''
        self.Manufacturer = 0
        self.OBUVersion = 0
        self.RegType = 0
        self.DriverIDType = 2
        self.FileNumber = 0
        self.FileInfo = []
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.MonitorData = MonitorStructType2(pdu[:30], 'pdu')
        payload = struct.unpack_from('<15s15sBQBBB', pdu[30:30+42])
        self.IMSI = payload[0].decode().rstrip('\0')
        self.IMEI = payload[1].decode().rstrip('\0')
        self.Manufacturer = payload[2]
        self.OBUVersion = payload[3]
        self.RegType = payload[4]
        self.DriverIDType = payload[5]
        self.FileNumber = payload[6]
        for i in range(self.FileNumber):
            file_info = FileStruct(pdu[72+(10*i):72+(10*i)+10], 'pdu')
            self.FileInfo.append(file_info)
        self.self_assert()

    def to_pdu(self) -> bytes:
        self.self_assert()
        IMSI = str.encode(self.IMSI)
        IMEI = str.encode(self.IMEI)
        bMonitorData = self.MonitorData.to_pdu()
        bFileInfo = bytes()
        for info in self.FileInfo:
            bFileInfo += info.to_pdu()
        self.FileNumber = len(self.FileInfo)
        bpayloads = struct.pack('<15s15sBQBBB', IMSI, IMEI, self.Manufacturer, self.OBUVersion,
                                self.RegType, self.DriverIDType, self.FileNumber)

        return bMonitorData + bpayloads + bFileInfo

    def from_dict(self, input_dict: dict):
        self.MonitorData = MonitorStructType2(input_dict['MonitorData'], 'dict')
        self.IMSI = input_dict['IMSI']
        self.IMEI = input_dict['IMEI']
        self.Manufacturer = input_dict['Manufacturer']
        self.OBUVersion = input_dict['OBUVersion']
        self.RegType = input_dict['RegType']
        self.DriverIDType = input_dict['DriverIDType']
        self.FileNumber = input_dict['FileNumber']
        self.FileInfo = [FileStruct(info, 'dict') for info in input_dict['FileInfo']]
        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        self.FileNumber = len(self.FileInfo)
        r = {
            'MonitorData': self.MonitorData.to_dict(),
            'IMSI': self.IMSI,
            'IMEI': self.IMEI,
            'Manufacturer': self.Manufacturer,
            'OBUVersion': self.OBUVersion,
            'RegType': self.RegType,
            'DriverIDType': self.DriverIDType,
            'FileNumber': self.FileNumber,
            'FileInfo': [info.to_dict() for info in self.FileInfo]
        }
        return r

    def from_default(self):
        pass

    def self_assert(self):
        pass
