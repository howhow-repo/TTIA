import struct
from .op_payload_base import OpPayloadBase


class OpRegDownlink(OpPayloadBase):
    message_id = 0x01

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HHBBBBBB32sB32sHHB', pdu)
        self.MessageGroupZoneID = payload[0]
        self.MessageGroupCasID = payload[1]
        self.WeekendBootTimeh = payload[2]
        self.WeekendBootTimem = payload[3]
        self.WeekendBootTimes = payload[4]
        self.WeekendShutdownTimeh = payload[5]
        self.WeekendShutdownTimem = payload[6]
        self.WeekendShutdownTimes = payload[7]
        self.District = (payload[8]).decode('big5').rstrip('\x00')
        self.MsgStopDelay = payload[9]
        self.BootMessage = (payload[10]).decode('big5').rstrip('\x00')
        self.IdleTime = payload[11]
        self.EventReportPeriod = payload[12]
        self.WeekDay = payload[13]

    def to_pdu(self):
        return struct.pack('<HHBBBBBB32sB32sHHB',
                           self.MessageGroupZoneID,self.MessageGroupCasID,
                           self.WeekendBootTimeh,self.WeekendBootTimem, self.WeekendBootTimes,
                           self.WeekendShutdownTimeh,self.WeekendShutdownTimem,self.WeekendShutdownTimes,
                           self.District.encode("big5"), self.MsgStopDelay,
                           self.BootMessage.encode("big5"),
                           self.IdleTime,
                           self.EventReportPeriod,
                           self.WeekDay,
                           )

    def from_dict(self, json):
        self.MessageGroupZoneID = json['MessageGroupZoneID']
        self.MessageGroupCasID = json['MessageGroupCasID']
        self.WeekendBootTimeh = json['WeekendBootTimeh']
        self.WeekendBootTimem = json['WeekendBootTimem']
        self.WeekendBootTimes = json['WeekendBootTimes']
        self.WeekendShutdownTimeh = json['WeekendShutdownTimeh']
        self.WeekendShutdownTimem = json['WeekendShutdownTimem']
        self.WeekendShutdownTimes = json['WeekendShutdownTimes']
        self.District = json['District']
        self.MsgStopDelay = json['MsgStopDelay']
        self.BootMessage = json['BootMessage']
        self.IdleTime = json['IdleTime']
        self.EventReportPeriod = json['EventReportPeriod']
        self.WeekDay = json['WeekDay']

    def to_dict(self):
        r = {
            'MessageGroupZoneID': self.MessageGroupZoneID,
            'MessageGroupCasID': self.MessageGroupCasID,
            'WeekendBootTimeh': self.WeekendBootTimeh,
            'WeekendBootTimem': self.WeekendBootTimem,
            'WeekendBootTimes': self.WeekendBootTimes,
            'WeekendShutdownTimeh': self.WeekendShutdownTimeh,
            'WeekendShutdownTimem': self.WeekendShutdownTimem,
            'WeekendShutdownTimes': self.WeekendShutdownTimes,
            'District': self.District,
            'MsgStopDelay': self.MsgStopDelay,
            'BootMessage': self.BootMessage,
            'IdleTime': self.IdleTime,
            'EventReportPeriod': self.EventReportPeriod,
            'WeekDay': self.WeekDay,
        }
        return r

    def from_default(self):
        self.MessageGroupZoneID = 0
        self.MessageGroupCasID = 0
        self.WeekendBootTimeh = 16
        self.WeekendBootTimem = 0
        self.WeekendBootTimes = 0
        self.WeekendShutdownTimeh = 15
        self.WeekendShutdownTimem = 0
        self.WeekendShutdownTimes = 0
        self.District = ''
        self.MsgStopDelay = 2
        self.BootMessage = ''
        self.IdleTime = 300
        self.EventReportPeriod = 300
        self.WeekDay = 1
