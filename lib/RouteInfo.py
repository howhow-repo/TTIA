from .TTIA_stop_message import TTIABusStopMessage


class RouteInfo:
    def __init__(self, setting_config):
        self.rrid = None
        self.sid = None
        self.dir = None
        self.gid = None
        self.seqno = None
        self.rname = None
        self.rename = None
        self.from_dict(setting_config)

    def from_dict(self, setting_config: dict):
        for item in self.__dict__:
            if item in setting_config.keys():
                self.__setattr__(item, setting_config[item])

    def to_dict(self):
        r = self.__dict__.copy()
        return r

    def to_ttia(self, stop_id: int, seq: int):
        msg = TTIABusStopMessage(0x0B, 'default')
        msg.header.StopID = stop_id
        if not self.rrid:
            msg.payload.RouteID = 0
        if not self.rname:
            msg.payload.PathCName = ''
        if not self.rename:
            msg.payload.PathEName = ''
        if not self.seqno:
            msg.payload.Sequence = 0
        else:
            msg.payload.Sequence = seq
        return msg
