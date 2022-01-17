class MessageBase:
    def __init__(self, init_data, init_type):
        """
        To init every TTIA Message, you have to define the raw data and type with 'pdu' or 'json'
        :param init_data:
        :param init_type:
            'pdu' or 'json'
        """
        if init_type == 'pdu':
            self.from_pdu(init_data)
        elif init_type == 'json':
            self.from_json(init_data)

    def from_pdu(self, pdu, offset=0):
        raise NotImplementedError

    def to_pdu(self):
        raise NotImplementedError

    def from_json(self, json):
        raise NotImplementedError

    def to_json(self):
        raise NotImplementedError


class MessageConstants:
    ProtocolID = "IBST"
    ProtocolVer = 0x01
