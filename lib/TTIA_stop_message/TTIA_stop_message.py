from abc import ABC

from .message_base import MessageBase
from .header import Header
from .payloadcreator import PayloadCreator
from .optionpayloadcreater import OptionPayloadCreater


def is_json_format(msg):
    if 'header' in msg and 'payload' in msg:
        return True
    return False


class TTIABusStopMessage:
    def __init__(self, init_data, init_type):
        """
        :param init_data:
            bytes like obj if init_type == 'pdu'
            dict obj if init_type == 'json'
            message id (int) if init_type == 'default'
        :param init_type:
            str: 'pdu' or 'json' or 'default'
        """
        self.header = None
        self.payload = None
        self.option_payload = None

        if init_type == 'pdu':
            self.from_pdu(init_data)
        elif init_type == 'json':
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
        if len(pdu) < 20:
            raise ValueError("input pdu is not long enough")

        self.header = Header(init_data=pdu[:20], init_type='pdu')

        if self.header.Len > len(pdu[20:]):
            raise ValueError(f"input pdu has wrong payload length. \n"
                             f"header.Len: {self.header.Len}, payload+option payload len:{len(pdu[20:])}")

        self.payload = PayloadCreator.create_payload_obj('pdu', pdu[20:20 + self.header.Len], self.header.MessageID)
        self.option_payload = OptionPayloadCreater.pdu_create_option_payload_obj(pdu[20 + self.header.Len:], self.header.MessageID)

    def to_pdu(self):
        payload_pdu = self.payload.to_pdu()
        option_payload_pdu = self.option_payload.to_pdu()
        self.header.Len = len(payload_pdu)
        return self.header.to_pdu() + payload_pdu + option_payload_pdu

    def from_dict(self, json):
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

        self.header.from_dict(json['header'])
        self.payload = PayloadCreator.create_payload_obj('json', json['payload'], self.header.MessageID)
        self.option_payload = OptionPayloadCreater.json_create_option_payload_obj(json['payload'], self.header.MessageID)

    def to_dict(self):
        self.header.Len = len(self.payload.to_pdu())
        j = {
            'header': self.header.to_dict(),
            'payload': self.payload.to_dict(),
            'option_payload': self.option_payload.to_dict()
        }
        return j

    def from_default(self, message_id: int):
        self.header = Header(b'', 'default')
        self.payload = PayloadCreator.create_payload_obj('default', b'', message_id)
        payload_pdu = self.payload.to_pdu()
        self.header.Len = len(payload_pdu)
        self.option_payload = OptionPayloadCreater.default_create_option_payload_obj(message_id)
