from .TTIA_stop_message import TTIABusStopMessage


class RouteInfo:
    def __init__(self, setting_config):
        self.rrid = 0
        self.sid = None
        self.dir = None
        self.gid = None
        self.seqno = 0
        self.rname = ''
        self.rename = ''
        self.from_dict(setting_config)

    def from_dict(self, setting_config: dict):
        for item in self.__dict__:
            if item in setting_config.keys() and setting_config[item] is not None:
                self.__setattr__(item, setting_config[item])

    def to_dict(self):
        r = self.__dict__.copy()
        return r

    def to_ttia(self, stop_id: int, seq: int):
        msg = TTIABusStopMessage(0x0B, 'default')
        msg.header.StopID = stop_id
        msg.payload.RouteID = self.rrid
        msg.payload.PathCName = self.rname
        msg.payload.PathEName = self.rename
        msg.payload.Sequence = seq
        return msg
