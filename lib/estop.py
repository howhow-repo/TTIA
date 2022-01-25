from .route_info import RouteInfo


class EStop:
    def __init__(self, setting_config: dict):

        # setting properties (check TTIA estop message id 0x01)
        self.StopID = None
        self.Provider = None
        self.IMSI = ""
        self.IMEI = ""
        self.StopCName = ""
        self.StopEName = ""
        self.Latitude = None
        self.Longitude = None
        self.TypeID = None
        self.BootTime = None
        self.ShutdownTime = None
        self.IdleMessage = ""
        self.DisplayMode = None
        self.MessageGroupID = None
        self.TextRollingSpeed = 0
        self.DistanceFunctionMode = 0
        self.ReportPeriod = 0
        self.LightSet = 0

        # setting optional properties (check TTIA estop message id 0x01)
        self.MessageGroupZoneID = None
        self.MessageGroupCasID = None
        self.WeekendBootTime = None
        self.WeekendShutdownTime = None
        self.District = None
        self.MsgStopDelay = 0
        self.BootMessage = ""
        self.IdleTime = None
        self.EventReportPeriod = None
        self.WeekDay = None

        # customise properties
        self.routelist = []
        self.address = None
        self.ready = False
        self.update_intent = None

        self.from_dict(setting_config)

    def from_dict(self, setting_config: dict):
        for item in self.__dict__:
            if item in setting_config.keys():
                self.__setattr__(item, setting_config[item])

        if "routelist" in setting_config.keys():
            self.routelist = []
            for route_info in setting_config['routelist']:
                self.routelist.append(RouteInfo(route_info))
            del setting_config['routelist']

    def to_dict(self):
        r = self.__dict__
        r['routelist'] = [route_info.to_dict() for route_info in self.routelist]
        return r

