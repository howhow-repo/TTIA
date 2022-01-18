import struct


class ReportStopNameDownlink:
    def __init__(self):
        self.RouteID = 0
        self.PathCName = ''
        self.PathEName = ''
        self.Sequence = 0

    def pack(self):
        PathCName = bytearray(self.PathCName.encode("big5"))
        PathEName = bytearray(self.PathEName.encode("big5"))
        return struct.pack('<H12s12sH', self.RouteID, PathCName, PathEName, self.Sequence)