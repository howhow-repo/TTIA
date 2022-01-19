from .optional_payload import *


class OptionPayloadCreater:
    @classmethod
    def pdu_create_option_payload_obj(cls, payload_pdu, message_id):
        if message_id == 0x01:  # 註冊請求訊息
            return OpRegDownlink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x05:
            # TODO
            return OpEmpty(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x07:
            return OpReportUpdateBusinfoDownlink(init_data=payload_pdu, init_type='pdu')
        else:
            return OpEmpty(init_data=payload_pdu, init_type='pdu')

    @classmethod
    def json_create_option_payload_obj(cls, payload_json, message_id):
        if message_id == 0x01:  # 註冊請求訊息
            return OpRegDownlink(init_data=payload_json, init_type='json')
        elif message_id == 0x05:
            # TODO
            return OpEmpty(init_data=payload_json, init_type='json')
        elif message_id == 0x07:
            return OpReportUpdateBusinfoDownlink(init_data=payload_json, init_type='json')
        else:
            return OpEmpty(init_data=payload_json, init_type='json')

    @classmethod
    def default_create_option_payload_obj(cls, message_id):
        if message_id == 0x01:  # 註冊請求訊息
            return OpRegDownlink(init_data=b'', init_type='json')
        elif message_id == 0x05:
            # TODO
            return OpEmpty(init_data=b'', init_type='json')
        elif message_id == 0x07:
            return OpReportUpdateBusinfoDownlink(init_data=b'', init_type='default')
        else:
            return OpEmpty(init_data=b'', init_type='default')