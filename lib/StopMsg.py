class StopMsg:
    def __init__(self):
        self.id = None
        self.gid = None
        self.tagid = None
        self.msg = ""
        self.updatetime = None
        self.expiretime = None

    def from_dict(self, setting_config: dict):
        for item in self.__dict__:
            if item in setting_config.keys():
                self.__setattr__(item, setting_config[item])

        return self
