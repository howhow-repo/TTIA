from abc import ABC

from .message_base import MessageBase
from .header import Header
from .payloadcreator import PayloadCreator


def is_pdu_format(pdu):
    if len(pdu) < 20:
        return False
    header = Header(init_data=pdu[:20], init_type='pdu')

    print(len(pdu))
    print(header.Len)
    print(len(pdu[20:]))

    if header.Len < len(pdu[20:]):
        return False
    return True


def is_json_format(msg):
    if 'header' in msg and 'payload' in msg:
        return True
    return False


class TTIAStopMessage(MessageBase, ABC):
    def __init__(self, init_data, init_type):
        super().__init__(init_data, init_type)

    def from_pdu(self, pdu, offset=0):
        """
        Follow TTIA Stop protocol, set input UDP binary message to python obj.

        :param pdu:
            Check TTIA Stop Protocol, length must longer than 20 bytes; Len in header must match length of payload.
        :param offset:
            offset of unpacking pdu.
        :return:

        """
        if not is_pdu_format(pdu):
            raise ValueError("input pdu has wrong format.")

        self.header = Header(init_data=pdu[:20], init_type='pdu')
        self.payload = PayloadCreator.pdu_create_payload_obj(pdu[20:20 + self.header.Len], self.header.MessageID)
        self.option_payload = pdu[20 + self.header.Len + 1:]

    def to_pdu(self):
        return self.header.to_pdu() + self.payload.to_pdu()

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
        j = {
            'header': self.header.to_json(),
            'payload': self.payload.to_json(),
            'option_payload': self.option_payload
        }
        return j