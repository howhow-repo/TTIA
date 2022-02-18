from .TTIA_stop_message import TTIABusStopMessage


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

    def to_ttia(self, stop_id: int, MsgNo: int = 0):
        msg = TTIABusStopMessage(0x05, 'default')
        msg.header.StopID = stop_id
        if self.tagid:
            msg.payload.MsgTag = self.tagid
        msg.payload.MsgNo = MsgNo
        msg.payload.MsgContent = self.msg
        return msg
