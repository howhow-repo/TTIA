import struct
from ..message_base import MessageBase


class FileStruct(MessageBase):
    def __init__(self, init_data, init_type: str):
        self.FileName = ''
        self.FileVersion = ''
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        self.FileName = (struct.unpack('<4s', pdu[:4])[0]).decode().rstrip('\0')
        self.FileVersion = (struct.unpack('<6s', pdu[4:])[0]).decode().rstrip('\0')

    def to_pdu(self) -> bytes:
        FileName = str.encode(self.FileName)
        FileVersion = str.encode(self.FileVersion)
        return struct.pack('<4s6s', FileName, FileVersion)

    def from_dict(self, input_dict: dict):
        self.FileName = str.encode(input_dict['FileName'])
        self.FileVersion = str.encode(input_dict['FileVersion'])

    def to_dict(self) -> dict:
        r = {
            'FileName': self.FileName,
            'FileVersion': self.FileVersion,
        }
        return r

    def from_default(self):
        pass
