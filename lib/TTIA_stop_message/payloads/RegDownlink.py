import struct

from .payload_base import PayloadBase


class RegDownlink(PayloadBase):
    def from_pdu(self, pdu, offset=0):
        payload = struct.unpack_from('<BH32s32sBBHBBHHBBBBBB32sBBBBBBBBBH', pdu, offset)
        self.Result = payload[0]
        self.MsgTag = payload[1]  # 系統訊息
        self.StopCName = payload[2]
        self.StopEName = payload[3]
        self.LongitudeDu = payload[4]
        self.LongitudeFen = payload[5]
        self.LongitudeMiao = payload[6]
        self.LatitudeDu = payload[7]
        self.LatitudeFen = payload[8]
        self.LatitudeMiao = payload[9]
        self.TypeID = payload[10]
        self.BootTimeh = payload[11]
        self.BootTimem = payload[12]
        self.BootTimes = payload[13]
        self.ShutdownTimeh = payload[14]
        self.ShutdownTimem = payload[15]
        self.ShutdownTimes = payload[16]
        self.MessageGroupID = payload[17]
        self.IdleMessage = payload[18]
        self.Year = payload[19] + 2000
        self.Month = payload[20]
        self.Day = payload[21]
        self.Hour = payload[22]
        self.Minute = payload[23]
        self.Second = payload[24]
        self.DisplayMode = payload[25]
        self.TextRollingSpeed = payload[26]
        self.DistanceFunctionMode = payload[27]
        self.ReportPeriod = payload[28]

    def from_json(self, json):
        self.Result = 0
        self.MsgTag = 0  # 系統訊息
        self.StopCName = ''
        self.StopEName = ''
        self.LongitudeDu = 0
        self.LongitudeFen = 0
        self.LongitudeMiao = 0
        self.LatitudeDu = 0
        self.LatitudeFen = 0
        self.LatitudeMiao = 0
        self.TypeID = 0
        self.BootTimeh = 0
        self.BootTimem = 0
        self.BootTimes = 0
        self.ShutdownTimeh = 0
        self.ShutdownTimem = 0
        self.ShutdownTimes = 0
        self.MessageGroupID = 0
        self.IdleMessage = ''
        self.Year = 0
        self.Month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.DisplayMode = 0
        self.TextRollingSpeed = 0
        self.DistanceFunctionMode = 0
        self.ReportPeriod = 0

    def to_pdu(self):
        StopCName1 = bytearray()
        StopCName1.extend(self.StopCName.encode("big5"))
        StopEName1 = bytearray()
        StopEName1.extend(self.StopEName.encode("big5"))
        IdleMessage1 = bytearray()
        IdleMessage1.extend(self.IdleMessage.encode("big5"))
        return struct.pack('<BH32s32sBBHBBHHBBBBBB32sBBBBBBBBBH',
                           self.Result,
                           self.MsgTag,
                           StopCName1, StopEName1, self.LongitudeDu, self.LongitudeFen, self.LongitudeMiao,
                           self.LatitudeDu, self.LatitudeFen, self.LatitudeMiao,
                           self.TypeID, self.BootTimeh, self.BootTimem, self.BootTimes, self.ShutdownTimeh,
                           self.ShutdownTimem, self.ShutdownTimes, IdleMessage1,
                           (self.Year - 2000), self.Month, self.Day, self.Hour, self.Minute, self.Second,
                           self.DisplayMode, self.TextRollingSpeed, self.DistanceFunctionMode, self.ReportPeriod
                           )
