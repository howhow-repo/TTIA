class MessageBase:
    MessageID = None

    def __init__(self, init_data, init_type: str):
        """
        To init every TTIA Message, you have to define the raw data and type with 'pdu' or 'json'
        :param init_data:
            bytes like object, looks like: b'IBST\x01\x01\xff\xff....'
        :param init_type:
            'pdu' or 'json' or 'default'
        """
        if init_type == 'pdu':
            self.from_pdu(init_data)
        elif init_type == 'dict':
            self.from_dict(init_data)
        elif init_type == 'default':
            self.from_default()

    def from_pdu(self, pdu: bytes):
        raise NotImplementedError

    def to_pdu(self) -> bytes:
        raise NotImplementedError

    def from_dict(self, input_dict: dict):
        raise NotImplementedError

    def to_dict(self) -> dict:
        raise NotImplementedError

    def from_default(self):
        raise NotImplementedError

    def self_assert(self):
        pass

class MessageConstants:
    ProtocolID = 'APTS'
    ProtocolVer = 0x01
    CustomerID = 0x01


class MessageName:
    RegUplink = 0x00
    RegDownlink = 0x01
    ChangeRouteUplink = 0x02
    ChangeRouteDownlink = 0x03
    MonitorUplink = 0x04
    MonitorDownlink = 0x05
    SendCarMsgUplink = 0x06
    SendCarMsgDownlink = 0x07
    EventsUplink = 0x08
    EventsDownlink = 0x09
    PowerOffMsgUplink = 0x0A
    PowerOffMsgDownlink = 0x0B
    # 0xE0-0xEF: 業者自行定義
    ObstacleReportUplink = 0xF0
    ObstacleReportDownlink = 0xF1
    ODReportUplink = 0xF2
    ODReportDownlink = 0xF3
