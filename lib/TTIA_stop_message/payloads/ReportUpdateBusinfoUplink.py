import struct


class ReportUpdateBusinfoUplink:
    def __init__(self, buff=None, offset=0):
        header = struct.unpack_from('<BB', buff, offset)
        self.MsgStatus = header[0]
        self.Reserved = header[1]