from .route_info import RouteInfo


class EStop:
    def __init__(self, setting_config: dict):
        self.id = None
        self.imsi = ""
        self.name = ""
        self.ename = ""
        self.gid = None
        self.boottime = 0
        self.shutdowntime = 0
        self.idlemessage = ""
        self.textrollingspeed = 0
        self.distancefunctionmode = 0
        self.reportperiod = 0
        self.seqno = None
        self.dir = None
        self.tid = None
        self.vid = None
        self.routelist = []

        self.from_dict(setting_config)

    def from_dict(self, setting_config: dict):
        for item in self.__dict__:
            if item in setting_config.keys() :
                self.__setattr__(item, setting_config[item])

        if "routelist" in setting_config.keys():
            self.routelist = []
            for route_info in setting_config['routelist']:
                self.routelist.append(RouteInfo(route_info))
            del setting_config['routelist']


