from .message_base import MessageBase
from .payloads import *


class PayloadCreator:
    @classmethod
    def create_payload_obj(cls, payload, message_id: int) -> MessageBase:
        """
        :param payload:
            raw data of payload. It can be <bytes> / <dict> / None,
            with different data type, it will auto create payload obj.
            (depends on the para data type.)
        :param message_id:
            fill the message id in header
        :return:
            a payload object
        """
        if type(payload) == bytes:
            paras = {'init_data': payload, 'init_type': 'pdu'}
        elif type(payload) == dict:
            paras = {'init_data': payload, 'init_type': 'dict'}
        elif payload is None:
            paras = {'init_data': b'', 'init_type': 'default'}
        else:
            raise ValueError("No such payload raw data type, please use bytes or dict or None")

        if message_id == 0x00:  # 基本資料查詢訊息
            return RegUplink(**paras)
        elif message_id == 0x01:  # 基本資料設定訊息
            return RegDownlink(**paras)
        elif message_id == 0x02:  # 基本資料設定確認訊息
            return ReportBaseMsgTagUplink(**paras)
        elif message_id == 0x03:  # 定時回報訊息
            return ReportMsgcountUplink(**paras)
        elif message_id == 0x04:  # 定時回報確認訊息
            return ReportMsgcountDownlink(**paras)
        elif message_id == 0x05:  # 更新站牌文字訊息
            return ReportUpdateMsgTagDownlink(**paras)
        elif message_id == 0x06:  # 更新站牌文字確認訊息
            return ReportUpdateMsgTagUplink(**paras)
        elif message_id == 0x07:  # 更新即時公車資訊訊息
            return ReportUpdateBusinfoDownlink(**paras)
        elif message_id == 0x08:  # 更新即時公車資訊確認訊息
            return ReportUpdateBusinfoUplink(**paras)
        elif message_id == 0x09:  # 異常回報訊息
            return ReportAbnormalUplink(**paras)
        elif message_id == 0x0A:  # 異常回報確認訊息
            return ReportAbnormalDownlink(**paras)
        elif message_id == 0x0B:  # 路線資料設定訊息
            return ReportUpdateRouteinfoDownlink(**paras)
        elif message_id == 0x0C:  # 路線資料設定訊息
            return ReportUpdateRouteinfoUplink(**paras)
        elif message_id == 0x0D:  # 亮度設定
            return ReportSetBrightnessDownlink(**paras)
        elif message_id == 0x0E:  # 亮度設定確認
            return ReportSetBrightnessUplink(**paras)
        elif message_id == 0x10:  # 重開通知訊息(系統軟體重置)
            return ReportRebootDownlink(**paras)
        elif message_id == 0x11:  # 重開確認訊息
            return ReportRebootUplink(**paras)
        elif message_id == 0x12:  # 動態圖示通知訊息
            return ReportUpdateGifDownlink(**paras)
        elif message_id == 0x13:  # 動態圖示確認訊息
            return ReportUpdateGifUplink(**paras)
        else:
            raise NotImplementedError("no message payload define.")
