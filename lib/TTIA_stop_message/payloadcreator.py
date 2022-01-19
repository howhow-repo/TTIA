from .message_base import MessageBase
from .payloads import *


class PayloadCreator:
    @classmethod
    def create_payload_obj(cls, payload_type: str, payload, message_id) -> MessageBase:
        """
        :param payload_type:
            'pdu' or 'json' or 'default'
            depends on the type of your payload is.
        :param payload:
            raw data of payload. It can be byte like / dict / nothong, depends on the decode type you want.
        :param message_id:
            fill the message id in header
        :return:
            a payload object
        """
        if payload_type == 'pdu':
            paras = {'init_data': payload, 'init_type': 'pdu'}
        elif payload_type == 'json':
            paras = {'init_data': payload, 'init_type': 'json'}
        elif payload_type == 'default':
            paras = {'init_data': b'', 'init_type': 'default'}
        else:
            raise ValueError("No such payload raw data")

        if message_id == 0x00:  # 註冊請求訊息
            return RegUplink(**paras)
        elif message_id == 0x01:  # 基本資料設定確認訊息
            return RegDownlink(**paras)
        elif message_id == 0x02:  # 基本資料設定確認訊息
            return ReportBaseMsgTagUplink(**paras)
        elif message_id == 0x03:  # 定時回報確認訊息
            return ReportMsgcountUplink(**paras)
        elif message_id == 0x04:  # 定時回報確認訊息
            return ReportMsgcountDownlink(**paras)
        elif message_id == 0x05:  # 定時回報確認訊息
            return ReportUpdateMsgTagDownlink(**paras)
        elif message_id == 0x06:  # 更新站牌文字確認訊息
            return ReportUpdateMsgTagUplink(**paras)
        elif message_id == 0x07:  # 更新站牌文字確認訊息
            return ReportUpdateBusinfoDownlink(**paras)
        elif message_id == 0x08:  # 更新即時公車資訊確認訊息
            return ReportUpdateBusinfoUplink(**paras)
        elif message_id == 0x09:  # 異常回報確認訊息
            return ReportAbnormalUplink(**paras)
        elif message_id == 0x0A:  # 異常回報確認訊息
            return ReportAbnormalDownlink(**paras)
        elif message_id == 0x0B:  # 異常回報確認訊息
            return ReportUpdateRouteinfoDownlink(**paras)
        elif message_id == 0x0C:  #
            return ReportUpdateRouteinfoUplink(**paras)
        elif message_id == 0x0D:  #
            return ReportSetBrightnessDownlink(**paras)
        elif message_id == 0x0E:  #
            return ReportSetBrightnessUplink(**paras)
        elif message_id == 0x10:  #
            return ReportRebootDownlink(**paras)
        elif message_id == 0x11:  #
            return ReportRebootUplink(**paras)
        elif message_id == 0x12:  #
            return ReportUpdateGifDownlink(**paras)
        elif message_id == 0x13:  #
            return ReportUpdateGifUplink(**paras)
        else:
            raise NotImplementedError("no message payload define.")
