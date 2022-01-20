class MessageBase:
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

    def from_pdu(self, pdu):
        raise NotImplementedError

    def to_pdu(self):
        raise NotImplementedError

    def from_dict(self, json):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    def from_default(self):
        raise NotImplementedError


class MessageConstants:
    ProtocolID = "IBST"
    ProtocolVer = 0x01
