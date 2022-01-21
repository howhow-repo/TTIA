import struct
from .payload_base import PayloadBase


class ReportAbnormalUplink(PayloadBase):
    message_id = 0x09
    message_cname = "異常回報訊息"

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<BBBBBBBBBBBBBB', pdu)
        self.StatusCode = payload[0]
        self.Type = payload[1]
        self.TransYear = payload[2] + 2000
        self.TransMonth = payload[3]
        self.TransDay = payload[4]
        self.TransHour = payload[5]
        self.TransMinute = payload[6]
        self.TransSecond = payload[7]
        self.RcvYear = payload[8] + 2000
        self.RcvMonth = payload[9]
        self.RcvDay = payload[10]
        self.RcvHour = payload[11]
        self.RcvMinute = payload[12]
        self.RcvSecond = payload[13]

    def to_pdu(self):
        return struct.pack('<BBBBBBBBBBBBBB',
                           self.StatusCode,
                           self.Type,
                           self.TransYear - 2000,
                           self.TransMonth,
                           self.TransDay,
                           self.TransHour,
                           self.TransMinute,
                           self.TransSecond,
                           self.RcvYear - 2000,
                           self.RcvMonth,
                           self.RcvDay,
                           self.RcvHour,
                           self.RcvMinute,
                           self.RcvSecond)

    def from_dict(self, input_dict):
        self.StatusCode = input_dict['StatusCode']
        self.Type = input_dict['Type']
        self.TransYear = input_dict['TransYear']
        self.TransMonth = input_dict['TransMonth']
        self.TransDay = input_dict['TransDay']
        self.TransHour = input_dict['TransHour']
        self.TransMinute = input_dict['TransMinute']
        self.TransSecond = input_dict['TransSecond']
        self.RcvYear = input_dict['RcvYear']
        self.RcvMonth = input_dict['RcvMonth']
        self.RcvDay = input_dict['RcvDay']
        self.RcvHour = input_dict['RcvHour']
        self.RcvMinute = input_dict['RcvMinute']
        self.RcvSecond= input_dict['RcvSecond']

    def to_dict(self):
        r = {
            'StatusCode': self.StatusCode,
            'Type':self.Type,
            'TransYear':self.TransYear,
            'TransMonth':self.TransMonth,
            'TransDay':self.TransDay,
            'TransHour':self.TransHour,
            'TransMinute':self.TransMinute,
            'TransSecond':self.TransSecond,
            'RcvYear':self.RcvYear,
            'RcvMonth':self.RcvMonth,
            'RcvDay':self.RcvDay,
            'RcvHour':self.RcvHour,
            'RcvMinute':self.RcvMinute,
            'RcvSecond':self.RcvSecond
        }
        return r

    def from_default(self):
        self.StatusCode = 0
        self.Type = 1
        self.TransYear = 2000
        self.TransMonth = 1
        self.TransDay = 1
        self.TransHour = 0
        self.TransMinute = 0
        self.TransSecond = 0
        self.RcvYear = 2000
        self.RcvMonth = 1
        self.RcvDay = 1
        self.RcvHour = 0
        self.RcvMinute = 0
        self.RcvSecond = 0
