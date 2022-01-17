import struct


class ReportBaseMsgTagUplink:
    def __init__(self, buff=None, offset=0):
        header = struct.unpack_from('<HBB', buff, offset)
        self.MsgTag = header[0]
        self.MsgStatus = header[1]
        self.Reserved = header[2]