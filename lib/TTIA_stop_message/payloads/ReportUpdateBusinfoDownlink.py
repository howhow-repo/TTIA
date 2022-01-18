import struct

from .payload_base import PayloadBase


class ReportUpdateBusinfoDownlink(PayloadBase):
    message_id = 0x07

    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu):
        payload = struct.unpack_from('<HHQQBHHBBBBBBBBBBBBBBB12s12s24s24s', pdu)
        self.RouteID = payload[0]
        self.BusID = payload[1]
        self.CurrentStop = payload[2]
        self.DestinationStop = payload[3]
        self.IsLastBus = payload[4]
        self.EstimateTime = payload[5]
        self.StopDistance = payload[6]
        self.Direction = payload[7]
        self.Type = payload[8]
        self.TransYear = payload[9] + 2000
        self.TransMonth = payload[10]
        self.TransDay = payload[11]
        self.TransHour = payload[12]
        self.TransMinute  = payload[13]
        self.TransSecond = payload[14]
        self.RcvYear = payload[15] + 2000
        self.RcvMonth = payload[16]
        self.RcvDay = payload[17]
        self.RcvHour = payload[18]
        self.RcvMinute = payload[19]
        self.RcvSecond = payload[20]
        self.Reserved = payload[21]

        self.Cinfo = bytearray(payload[22]).decode('big5')
        self.Einfo = bytearray(payload[23]).decode('ascii')
        self.RouteMsgCContent = bytearray(payload[24]).decode('big5')
        self.RouteMsgEContent = bytearray(payload[25]).decode('ascii')

    def to_pdu(self):
        return struct.pack('<HHQQBHHBBBBBBBBBBBBBBB12s12s24s24s', self.RouteID, self.BusID, self.CurrentStop,
                           self.DestinationStop, self.IsLastBus, self.EstimateTime, self.StopDistance,
                           self.Direction,
                           self.Type, self.TransYear - 2000, self.TransMonth, self.TransDay, self.TransHour,
                           self.TransMinute, self.TransSecond,
                           self.RcvYear - 2000, self.RcvMonth, self.RcvDay, self.RcvHour, self.RcvMinute,
                           self.RcvSecond, self.Reserved,
                           self.Cinfo.encode("big5"), self.Einfo.encode(), self.RouteMsgCContent.encode("big5"),
                           self.RouteMsgEContent.encode()
                           )

    def from_default(self):
        self.RouteID = 0
        self.BusID = 0
        self.CurrentStop = 0
        self.DestinationStop = 0
        self.IsLastBus = 0
        self.EstimateTime = 0
        self.StopDistance = 0
        self.Direction = 0
        self.Type = 0
        self.TransYear = 0
        self.TransMonth = 0
        self.TransDay = 0
        self.TransHour = 0
        self.TransMinute = 0
        self.TransSecond = 0
        self.RcvYear = 0
        self.RcvMonth = 0
        self.RcvDay = 0
        self.RcvHour = 0
        self.RcvMinute = 0
        self.RcvSecond = 0
        self.Reserved = 0
        self.min = 0
        self.Cinfo = ''
        self.Einfo = ''
        self.RouteMsgCContent = ''
        self.RouteMsgEContent = ''


