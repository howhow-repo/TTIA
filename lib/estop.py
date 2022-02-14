from datetime import time

from .route_info import RouteInfo


def deg_to_dms(deg):
    """
        經緯度表示法轉換
        按照文件，miao = 分的小數部分, 十進位非六十進位, 精度取４位數因此*10000
    """
    du = int(deg)
    md = abs(deg - du) * 60
    fen = int(md)
    miao = int((md - fen) * 10000)
    return [du, fen, miao]


class EStop:
    def __init__(self, setting_config: dict):

        # setting properties (check TTIA estop message id 0x01)
        self.StopID = None
        self.Provider = None
        self.IMSI = ""
        self.IMEI = ""
        self.StopCName = ""
        self.StopEName = ""
        self.Latitude = 0
        self.Longitude = 0
        self.TypeID = None
        self.BootTime = None
        self.ShutdownTime = None
        self.IdleMessage = ""
        self.DisplayMode = None
        self.MessageGroupID = None
        self.TextRollingSpeed = 0
        self.DistanceFunctionMode = 0
        self.ReportPeriod = 60

        # dynamic setting
        self.LightSet = 0
        self.SentCount = 0
        self.RevCount = 0
        self.MsgTag = None
        self.MsgNo = None
        self.MsgContent = ''
        self.MsgPriority = 0
        self.MsgType = 0

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
        self.routelist = []  # routes that pass through this stop
        self.address = None  # To keep the stop's ip address
        self.lasttime = None  # last report time
        self.ready = False
        self.abnormal_log = []

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

        if 'LongitudeDu' in setting_config.keys() \
                and 'LongitudeFen' in setting_config.keys() \
                and 'LongitudeMiao' in setting_config.keys():
            self.Longitude = setting_config['LongitudeDu'] + \
                             ((setting_config['LongitudeFen'] + (setting_config['LongitudeMiao']/10000))/60)

            self.Longitude = round(self.Longitude, 8)
        if 'LatitudeDu' in setting_config.keys() \
                and 'LatitudeFen' in setting_config.keys() \
                and 'LatitudeMiao' in setting_config.keys():
            self.Latitude = setting_config['LatitudeDu'] + \
                             ((setting_config['LatitudeFen'] + (setting_config['LatitudeMiao'] / 10000)) / 60)
            self.Latitude = round(self.Latitude, 8)

    def to_dict(self):
        r = self.__dict__.copy()
        r['routelist'] = [route_info.to_dict() for route_info in self.routelist]

        r['LongitudeDu'], r['LongitudeFen'], r['LongitudeMiao'] = deg_to_dms(abs(self.Longitude))
        r['LatitudeDu'], r['LatitudeFen'], r['LatitudeMiao'] = deg_to_dms(abs(self.Latitude))
        return r

    def to_json(self):
        r = self.to_dict()
        if self.BootTime:
            r['BootTime'] = f"{self.BootTime.hour}:{self.BootTime.minute}:{self.BootTime.second}"
        if self.ShutdownTime:
            r['ShutdownTime'] = f"{self.ShutdownTime.hour}:{self.ShutdownTime.minute}:{self.BootTime.second}"
        if len(self.abnormal_log) > 0:
            r['abnormal_log'] = [log.to_dict() for log in self.abnormal_log]
        return r
