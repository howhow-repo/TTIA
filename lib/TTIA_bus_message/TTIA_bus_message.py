from .header import Header
from .payloadcreator import PayloadCreator


def is_format(msg):
    if 'header' in msg and 'payload' in msg:
        return True
    return False


class TTIABusMessage:
    def __init__(self, init_data, init_type):
        """
        Use cases:
            Case1: init_data is bytes like pdu:
                init_data = <bytes like obj>, init_type='pdu'

            Case2: init_data is json like dict:
                init_data = <dict>, init_type='dict'

            Case3: Init an empty message with default property/value:
                init_data = <don't care>, init_type='default'
        """
        self.header = None
        self.payload = None

        if init_type == 'pdu':
            self.from_pdu(init_data)
        elif init_type == 'dict':
            self.from_dict(init_data)
        elif init_type == 'default':
            self.from_default(init_data)

    def from_pdu(self, pdu: bytes):
        """
        Follow TTIA Stop protocol, set input UDP binary message to python obj.

        :param pdu:
            Base on TTIA Stop Protocol, length must longer than 20 bytes; Len in header must match length of payload.
        :param offset:
            offset of unpacking pdu.
        :return:

        """
        assert len(pdu) >= 20, "Every message with header should longer then 20 bytes."

        self.header = Header(init_data=pdu[:20], init_type='pdu')

        assert len(pdu[20:]) >= self.header.Len, "payload length must longer than Len in header."

        try:
            self.payload = PayloadCreator.create_payload_obj(pdu[20:20 + self.header.Len], self.header.MessageID)
        except Exception as e:
            raise ValueError(f"Fail to init payload by given pdu. \n {e}")

    def to_pdu(self):
        payload_pdu = self.payload.to_pdu()
        self.header.Len = len(payload_pdu)
        return self.header.to_pdu() + payload_pdu

    def from_dict(self, dict):
        """
        :param dict:
            {
                "header":{<header_json_format>},
                "payload":{<payload_json_format>},
                "option_payload":{<option_payload_json_format>},
            }
        :return:

        """
        if not is_format(dict):
            raise ValueError("input json has no require keys. \n "
                             "Please check Your input is a dict like {'header':{...},'payload':{...}}")

        self.header = Header(init_data=dict['header'], init_type='dict')
        self.payload = PayloadCreator.create_payload_obj(dict['payload'], self.header.MessageID)

    def to_dict(self):
        self.header.Len = len(self.payload.to_pdu())
        j = {
            'header': self.header.to_dict(),
            'payload': self.payload.to_dict(),
        }
        return j

    def from_default(self, message_id: int):
        self.header = Header(b'', 'default')
        self.payload = PayloadCreator.create_payload_obj(None, message_id)
        payload_pdu = self.payload.to_pdu()

        self.header.MessageID = message_id
        self.header.Len = len(payload_pdu)
