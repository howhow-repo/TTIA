import struct


class ReportAbnormalUplink:
    def __init__(self, buff=None, offset=0):
        header = struct.unpack_from('<BBBBBBBBBBBBBB', buff, offset)
        self.StatusCode = header[0]
        self.Type = header[1]
        self.TransYear = header[2]
        self.TransMonth = header[3]
        self.TransDay = header[4]
        self.TransHour = header[5]
        self.TransMinute = header[6]
        self.TransSecond = header[7]
        self.RcvYear = header[8]
        self.RcvMonth = header[9]
        self.RcvDay = header[10]
        self.RcvHour = header[11]
        self.RcvMinute = header[12]
        self.RcvSecond = header[13]