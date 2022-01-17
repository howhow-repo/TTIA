import struct


class ReportUpdateMsgTagDownlink:
    def __init__(self, content=''):
        self.MsgTag = 0
        self.MsgNo = 0
        self.MsgContent = content

    def pack(self):
        MsgContent1 = bytearray()
        MsgContent1.extend(self.MsgContent.encode("big5"))
        return struct.pack('<HH160s', self.MsgTag, self.MsgNo, MsgContent1)
