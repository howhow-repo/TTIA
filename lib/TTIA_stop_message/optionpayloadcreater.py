from .optional_payload import *


class OptionPayloadCreater:
    @classmethod
    def create_option_payload_obj(cls, payload, message_id):
        if type(payload) == bytes:
            paras = {'init_data': payload, 'init_type': 'pdu'}
        elif type(payload) == dict:
            paras = {'init_data': payload, 'init_type': 'dict'}
        elif payload is None:
            paras = {'init_data': b'', 'init_type': 'default'}
        else:
            raise ValueError("No such payload raw data type, please use bytes or dict or None")

        if message_id == 0x01:  # 註冊請求訊息
            return OpRegDownlink(**paras)
        elif message_id == 0x05:
            return OpReportUpdateMsgTagDownlink(**paras)
        elif message_id == 0x07:
            return OpReportUpdateBusinfoDownlink(**paras)
        else:
            return OpEmpty(**paras)
