import struct


class ReportUpdateBusinfoDownlink:
    def __init__(self):
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

    def pack(self):
        return struct.pack('<HHQQBHHBBBBBBBBBBBBBBB12s12s24s24s', self.RouteID, self.BusID, self.CurrentStop,
                           self.DestinationStop, self.IsLastBus, self.EstimateTime, self.StopDistance, self.Direction,
                           self.Type, self.TransYear - 2000, self.TransMonth, self.TransDay, self.TransHour,
                           self.TransMinute, self.TransSecond,
                           self.RcvYear - 2000, self.RcvMonth, self.RcvDay, self.RcvHour, self.RcvMinute,
                           self.RcvSecond, self.Reserved,
                           self.Cinfo.encode("big5"), self.Einfo.encode(), self.RouteMsgCContent.encode("big5"),
                           self.RouteMsgEContent.encode()
                           )
