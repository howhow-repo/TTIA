import struct

from .payload_base import PayloadBase
from datetime import time


class RegDownlink(PayloadBase):
    message_id = 0x01
    message_cname = "基本資料設定訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu: bytes):
        payload = struct.unpack_from('<BH32s32sBBHBBHHBBBBBBB32sBBBBBBBBBH', pdu)
        self.Result = payload[0]
        self.MsgTag = payload[1]  # 系統訊息
        self.StopCName = (payload[2].decode('big5')).rstrip('\x00')
        self.StopEName = (payload[3].decode('ascii')).rstrip('\x00')
        self.LongitudeDu = payload[4]
        self.LongitudeFen = payload[5]
        self.LongitudeMiao = payload[6]
        self.LatitudeDu = payload[7]
        self.LatitudeFen = payload[8]
        self.LatitudeMiao = payload[9]
        self.TypeID = payload[10]
        self.BootTime = time(payload[11], payload[12], payload[13])
        self.ShutdownTime = time(payload[14], payload[15], payload[16])
        self.MessageGroupID = payload[17]
        self.IdleMessage = (payload[18].decode('big5')).rstrip('\x00')
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

    def to_pdu(self) -> bytes:
        StopCName = bytearray(self.StopCName.encode("big5"))
        assert len(StopCName) <= 32, "StopCName overflow, please make sure it beneath 32 bytes"
        StopEName = bytearray(self.StopEName.encode("ascii"))
        assert len(StopEName) <= 32, "StopEName overflow, please make sure it beneath 32 bytes"
        IdleMessage = bytearray(self.IdleMessage.encode("big5"))
        assert len(IdleMessage) <= 32, "IdleMessage overflow, please make sure it beneath 32 bytes"

        self.self_assert()

        return struct.pack('<BH32s32sBBHBBHHBBBBBBB32sBBBBBBBBBH',
                           self.Result, self.MsgTag,
                           StopCName, StopEName,
                           self.LongitudeDu, self.LongitudeFen, self.LongitudeMiao,
                           self.LatitudeDu, self.LatitudeFen, self.LatitudeMiao,
                           self.TypeID,
                           self.BootTime.hour, self.BootTime.minute, self.BootTime.second,
                           self.ShutdownTime.hour, self.ShutdownTime.minute, self.ShutdownTime.second,
                           self.MessageGroupID, IdleMessage,
                           (self.Year - 2000), self.Month, self.Day, self.Hour, self.Minute, self.Second,
                           self.DisplayMode, self.TextRollingSpeed, self.DistanceFunctionMode, self.ReportPeriod
                           )

    def from_dict(self, input_dict: dict):
        self.Result = input_dict['Result']
        self.MsgTag = input_dict['MsgTag']  # 系統訊息
        self.StopCName = input_dict['StopCName']
        self.StopEName = input_dict['StopEName']
        self.LongitudeDu = input_dict['LongitudeDu']
        self.LongitudeFen = input_dict['LongitudeFen']
        self.LongitudeMiao = input_dict['LongitudeMiao']
        self.LatitudeDu = input_dict['LatitudeDu']
        self.LatitudeFen = input_dict['LatitudeFen']
        self.LatitudeMiao = input_dict['LatitudeMiao']
        self.TypeID = input_dict['TypeID']
        self.BootTime = input_dict['BootTime']
        self.ShutdownTime = input_dict['ShutdownTime']
        self.MessageGroupID = input_dict['MessageGroupID']
        self.IdleMessage = input_dict['IdleMessage']
        self.Year = input_dict['Year']
        self.Month = input_dict['Month']
        self.Day = input_dict['Day']
        self.Hour = input_dict['Hour']
        self.Minute = input_dict['Minute']
        self.Second = input_dict['Second']
        self.DisplayMode = input_dict['DisplayMode']
        self.TextRollingSpeed = input_dict['TextRollingSpeed']
        self.DistanceFunctionMode = input_dict['DistanceFunctionMode']
        self.ReportPeriod = input_dict['ReportPeriod']

        self.self_assert()

    def to_dict(self) -> dict:
        self.self_assert()
        r = {
            'Result': self.Result,
            'MsgTag': self.MsgTag,
            'StopCName': self.StopCName,
            'StopEName': self.StopEName,
            'LongitudeDu': self.LongitudeDu,
            'LongitudeFen': self.LongitudeFen,
            'LongitudeMiao': self.LongitudeMiao,
            'LatitudeDu': self.LatitudeDu,
            'LatitudeFen': self.LatitudeFen,
            'LatitudeMiao': self.LatitudeMiao,
            'TypeID': self.TypeID,
            'BootTime': self.BootTime,
            'ShutdownTime': self.ShutdownTime,
            'MessageGroupID': self.MessageGroupID,
            'IdleMessage': self.IdleMessage,
            'Year': self.Year,
            'Month': self.Month,
            'Day': self.Day,
            'Hour': self.Hour,
            'Minute': self.Minute,
            'Second': self.Second,
            'DisplayMode': self.DisplayMode,
            'TextRollingSpeed': self.TextRollingSpeed,
            'DistanceFunctionMode': self.DistanceFunctionMode,
            'ReportPeriod': self.ReportPeriod,
        }
        return r

    def from_default(self):
        self.Result = 0
        self.MsgTag = 0
        self.StopCName = ''
        self.StopEName = ''
        self.LongitudeDu = 0
        self.LongitudeFen = 0
        self.LongitudeMiao = 0
        self.LatitudeDu = 0
        self.LatitudeFen = 0
        self.LatitudeMiao = 0
        self.TypeID = 0
        self.BootTime = time(0, 0, 0)
        self.ShutdownTime = time(0, 0, 0)
        self.MessageGroupID = 0
        self.IdleMessage = ''
        self.Year = 2000
        self.Month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.DisplayMode = 0
        self.TextRollingSpeed = 0
        self.DistanceFunctionMode = 0
        self.ReportPeriod = 60

    def self_assert(self):
        assert type(self.BootTime) == time, \
            "type of 'BootTime' must be <time>. Try using 'from datetime import time'"
        assert type(self.ShutdownTime) == time, \
            "type of 'ShutdownTime' must be <time>. Try using 'from datetime import time'"
        assert 0 <= self.TextRollingSpeed <= 9, "TextRollingSpeed should be 0~9; 0(min)~9(max)"
        assert self.DistanceFunctionMode in [0, 1], "DistanceFunctionMode should be 0~1; 0:disable; 1:enable"
