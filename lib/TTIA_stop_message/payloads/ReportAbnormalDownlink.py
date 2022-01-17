import struct


class ReportAbnormalDownlink:
    def __init__(self):
        self.MsgStatus = 1
        self.Reserved = 0

    def pack(self):
        return struct.pack('<BB', self.MsgStatus, self.Reserved)