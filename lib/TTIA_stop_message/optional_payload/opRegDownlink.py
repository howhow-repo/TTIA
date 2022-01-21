import struct
from .op_payload_base import OpPayloadBase
from datetime import time


class OpRegDownlink(OpPayloadBase):
    message_id = 0x01

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HHBBBBBB32sB32sHHB', pdu)
        self.MessageGroupZoneID = payload[0]
        self.MessageGroupCasID = payload[1]
        self.WeekendBootTime = time(payload[2], payload[3], payload[4])
        self.WeekendShutdownTime = time(payload[5], payload[6], payload[7])
        self.District = (payload[8]).decode('big5').rstrip('\x00')
        self.MsgStopDelay = payload[9]
        self.BootMessage = (payload[10]).decode('big5').rstrip('\x00')
        self.IdleTime = payload[11]
        self.EventReportPeriod = payload[12]
        self.WeekDay = payload[13]
        self.self_assert()

    def to_pdu(self):
        self.self_assert()
        District = bytearray(self.District.encode("big5"))
        assert len(District) <= 32, "District overflow, please make sure it beneath 32 bytes"
        BootMessage = bytearray(self.BootMessage.encode("big5"))
        assert len(BootMessage) <= 32, "BootMessage overflow, please make sure it beneath 32 bytes"

        return struct.pack('<HHBBBBBB32sB32sHHB',
                           self.MessageGroupZoneID, self.MessageGroupCasID,
                           self.WeekendBootTime.hour, self.WeekendBootTime.minute, self.WeekendBootTime.second,
                           self.WeekendShutdownTime.hour, self.WeekendShutdownTime.minute,
                           self.WeekendShutdownTime.second,
                           District, self.MsgStopDelay,
                           BootMessage,
                           self.IdleTime,
                           self.EventReportPeriod,
                           self.WeekDay,
                           )

    def from_dict(self, input_dict):
        self.MessageGroupZoneID = input_dict['MessageGroupZoneID']
        self.MessageGroupCasID = input_dict['MessageGroupCasID']
        self.WeekendBootTime = input_dict['WeekendBootTime']
        self.WeekendShutdownTime = input_dict['WeekendShutdownTime']
        self.District = input_dict['District']
        self.MsgStopDelay = input_dict['MsgStopDelay']
        self.BootMessage = input_dict['BootMessage']
        self.IdleTime = input_dict['IdleTime']
        self.EventReportPeriod = input_dict['EventReportPeriod']
        self.WeekDay = input_dict['WeekDay']
        self.self_assert()

    def to_dict(self):
        self.self_assert()
        r = {
            'MessageGroupZoneID': self.MessageGroupZoneID,
            'MessageGroupCasID': self.MessageGroupCasID,
            'WeekendBootTime': self.WeekendBootTime,
            'WeekendShutdownTime': self.WeekendShutdownTime,
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
        self.WeekendBootTime = time(0, 0, 0)
        self.WeekendShutdownTime = time(0, 0, 0)
        self.District = ''
        self.MsgStopDelay = 2
        self.BootMessage = ''
        self.IdleTime = 300
        self.EventReportPeriod = 300
        self.WeekDay = 1

    def self_assert(self):
        assert self.WeekDay in range(1, 7), "WeekDay should be 1~7, in which 1 is Sunday"
        assert type(self.WeekendBootTime) == time, \
            "type of 'WeekendBootTime' must be <time>. Try using 'from datetime import time'"
        assert type(self.WeekendShutdownTime) == time, \
            "type of 'WeekendShutdownTime' must be <time>. Try using 'from datetime import time'"
