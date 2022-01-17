import struct


class ReportMsgcountUplink:
    def __init__(self, buff=None, offset=0):
        header = struct.unpack_from('<HH', buff, offset)
        self.SentCount = header[0]
        self.RecvCount = header[1]