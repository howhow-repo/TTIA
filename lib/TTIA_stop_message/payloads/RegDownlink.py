import struct

from .payload_base import PayloadBase


class RegDownlink(PayloadBase):
    message_id = 0x01

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
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
        self.BootTimeh = payload[11]
        self.BootTimem = payload[12]
        self.BootTimes = payload[13]
        self.ShutdownTimeh = payload[14]
        self.ShutdownTimem = payload[15]
        self.ShutdownTimes = payload[16]
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

    def to_pdu(self):
        StopCName = bytearray(self.StopCName.encode("big5"))
        StopEName = bytearray(self.StopEName.encode("ascii"))
        IdleMessage = bytearray(self.IdleMessage.encode("big5"))
        return struct.pack('<BH32s32sBBHBBHHBBBBBBB32sBBBBBBBBBH',
                           self.Result,
                           self.MsgTag,
                           StopCName, StopEName, self.LongitudeDu, self.LongitudeFen, self.LongitudeMiao,
                           self.LatitudeDu, self.LatitudeFen, self.LatitudeMiao,
                           self.TypeID, self.BootTimeh, self.BootTimem, self.BootTimes, self.ShutdownTimeh,
                           self.ShutdownTimem, self.ShutdownTimes, self.MessageGroupID, IdleMessage,
                           (self.Year - 2000), self.Month, self.Day, self.Hour, self.Minute, self.Second,
                           self.DisplayMode, self.TextRollingSpeed, self.DistanceFunctionMode, self.ReportPeriod
                           )

    def from_dict(self, json):
        self.Result = json['Result']
        self.MsgTag = json['MsgTag']  # 系統訊息
        self.StopCName = json['StopCName']
        self.StopEName = json['StopEName']
        self.LongitudeDu = json['LongitudeDu']
        self.LongitudeFen = json['LongitudeFen']
        self.LongitudeMiao = json['LongitudeMiao']
        self.LatitudeDu = json['LatitudeDu']
        self.LatitudeFen = json['LatitudeFen']
        self.LatitudeMiao = json['LatitudeMiao']
        self.TypeID = json['TypeID']
        self.BootTimeh = json['BootTimeh']
        self.BootTimem = json['BootTimem']
        self.BootTimes = json['BootTimes']
        self.ShutdownTimeh = json['ShutdownTimeh']
        self.ShutdownTimem = json['ShutdownTimem']
        self.ShutdownTimes = json['ShutdownTimes']
        self.MessageGroupID = json['MessageGroupID']
        self.IdleMessage = json['IdleMessage']
        self.Year = json['Year']
        self.Month = json['Month']
        self.Day = json['Day']
        self.Hour = json['Hour']
        self.Minute = json['Minute']
        self.Second = json['Second']
        self.DisplayMode = json['DisplayMode']
        self.TextRollingSpeed = json['TextRollingSpeed']
        self.DistanceFunctionMode = json['DistanceFunctionMode']
        self.ReportPeriod = json['ReportPeriod']

    def to_dict(self):
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
            'BootTimeh': self.BootTimeh,
            'BootTimem': self.BootTimem,
            'BootTimes': self.BootTimes,
            'ShutdownTimeh': self.ShutdownTimeh,
            'ShutdownTimem': self.ShutdownTimem,
            'ShutdownTimes': self.ShutdownTimes,
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
        self.Year = 2000
        self.Month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.DisplayMode = 0
        self.TextRollingSpeed = 0
        self.DistanceFunctionMode = 0
        self.ReportPeriod = 0
