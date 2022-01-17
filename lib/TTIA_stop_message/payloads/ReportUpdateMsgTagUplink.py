import struct


class ReportUpdateMsgTagUplink:
    def __init__(self, buff=None, offset=0):
        header = struct.unpack_from('<HHBB', buff, offset)
        self.MsgTag = header[0]
        self.MsgNo = header[1]
        self.MsgStatus = header[2]
        self.Reserved = header[3]