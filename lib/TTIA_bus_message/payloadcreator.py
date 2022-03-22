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
            return RouteUplink(**paras)
        elif message_id == 0x03:  # 定時回報訊息
            return RouteDownlink(**paras)
        elif message_id == 0x04:  # 定時回報確認訊息
            return MonitorUplink(**paras)
        elif message_id == 0x05:  # 更新站牌文字訊息
            return MonitorDownlink(**paras)
        elif message_id == 0x06:  # 更新站牌文字確認訊息
            return SendCarMsgDownlink(**paras)
        elif message_id == 0x07:  # 更新即時公車資訊訊息
            return SendCarMsgUplink(**paras)
        elif message_id == 0x08:  # 更新即時公車資訊確認訊息
            return EventsUplink(**paras)
        elif message_id == 0x09:  # 異常回報訊息
            return EventsDownlink(**paras)
        elif message_id == 0x0A:  # 異常回報確認訊息
            return PoweroffUplink(**paras)
        elif message_id == 0x0B:  # 路線資料設定訊息
            return PoweroffDownlink(**paras)
        elif message_id == 0xF0:
            return ObstacleUplink(**paras)
        elif message_id == 0xF1:
            return ObstacleDownlink(**paras)
        elif message_id == 0xF2:
            return ODReportUplink(**paras)
        elif message_id == 0xE0:
            return DisseminateDownlink(**paras)
        elif message_id == 0xE1:
            return DisseminateUplink(**paras)
        else:
            raise NotImplementedError("no message payload define.")


