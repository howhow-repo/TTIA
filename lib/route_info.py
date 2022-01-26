class RouteInfo:
    def __init__(self, setting_config):
        self.rrid = None
        self.sid = None
        self.dir = None
        self.gid = None
        self.seqno = None
        self.rname = ''
        self.rename = ''
        self.from_dict(setting_config)

    def from_dict(self, setting_config: dict):
        for item in self.__dict__:
            if item in setting_config.keys():
                self.__setattr__(item, setting_config[item])

    def to_dict(self):
        r = self.__dict__.copy()
        return r
