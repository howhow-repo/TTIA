import struct


class ReportStopNameDownlink:
    def __init__(self):
        self.RouteID = 0
        self.PathCName = ''
        self.PathEName = ''
        self.Sequence = 0

    def pack(self):
        PathCName1 = bytearray()
        PathCName1.extend(self.PathCName.encode("big5"))
        PathEName1 = bytearray()
        PathEName1.extend(self.PathEName.encode("big5"))
        return struct.pack('<H12s12sH', self.RouteID, PathCName1, PathEName1, self.Sequence)