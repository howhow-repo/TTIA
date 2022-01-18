from abc import ABC

from .message_base import MessageBase
from .header import Header
from .payloadcreator import PayloadCreator


def is_json_format(msg):
    if 'header' in msg and 'payload' in msg:
        return True
    return False


class TTIABusStopMessage:
    def __init__(self, init_data, init_type):
        self.header = None
        self.payload = None
        self.option_payload = None

        if init_type == 'pdu':
            self.from_pdu(init_data)
        elif init_type == 'json':
            self.from_json(init_data)
        elif init_type == 'default':
            self.from_default(init_data)

    def from_pdu(self, pdu):
        """
        Follow TTIA Stop protocol, set input UDP binary message to python obj.

        :param pdu:
            Base on TTIA Stop Protocol, length must longer than 20 bytes; Len in header must match length of payload.
        :param offset:
            offset of unpacking pdu.
        :return:

        """
        if len(pdu) < 20:
            raise ValueError("input pdu is not long enough")

        self.header = Header(init_data=pdu[:20], init_type='pdu')

        if self.header.Len < len(pdu[20:]):
            raise ValueError("input pdu has wrong payload length.")

        self.payload = PayloadCreator.pdu_create_payload_obj(pdu[20:20 + self.header.Len], self.header.MessageID)

        if len(pdu) > 20 + self.header.Len:
            self.option_payload = pdu[20 + self.header.Len + 1:]
        else:
            self.option_payload = b''

    def to_pdu(self):
        payload_pdu = self.payload.to_pdu()
        self.header.Len = len(payload_pdu)
        return self.header.to_pdu() + payload_pdu

    def from_json(self, json):
        """
        :param json:
            {
                "header":{<header_json_format>},
                "payload":{<payload_json_format>},
                "option_payload":{<option_payload_json_format>},
            }
        :return:

        """
        if not is_json_format(json):
            raise ValueError("input json has wrong format.")

        self.header.from_json(json['header'])
        self.payload = PayloadCreator.json_create_payload_obj(json['payload'], self.header.MessageID)
        self.option_payload = json['option_payload']

    def to_json(self):
        self.header.Len = len(self.payload.to_pdu())
        j = {
            'header': self.header.to_json(),
            'payload': self.payload.to_json(),
            'option_payload': self.option_payload
        }
        return j

    def from_default(self, message_id: int):
        self.header = Header(b'', 'default')
        self.payload = PayloadCreator.default_create_payload_obj(message_id)
        payload_pdu = self.payload.to_pdu()
        self.header.Len = len(payload_pdu)
        self.option_payload = b''
