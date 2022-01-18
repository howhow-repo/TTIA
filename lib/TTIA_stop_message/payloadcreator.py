from .payloads import *

class PayloadCreator:

    @classmethod
    def pdu_create_payload_obj(cls, payload_pdu, message_id):
        if message_id == 0x00:  # 註冊請求訊息
            return RegUplink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x01:  # 基本資料設定確認訊息
            return RegDownlink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x02:  # 基本資料設定確認訊息
            return ReportBaseMsgTagUplink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x03:  # 定時回報確認訊息
            return ReportMsgcountUplink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x04:  # 定時回報確認訊息
            return ReportMsgcountDownlink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x05:  # 定時回報確認訊息
            return ReportUpdateMsgTagDownlink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x06:  # 更新站牌文字確認訊息
            return ReportUpdateMsgTagUplink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x07:  # 更新站牌文字確認訊息
            return ReportUpdateBusinfoDownlink(init_data=payload_pdu, init_type='pdu')
        elif message_id == 0x08:  # 更新即時公車資訊確認訊息
            pass
            # sendbuf = self.handleReportUpdateBusinfoUplink(TTIAHeaderdata, data)
            return
        elif message_id == 0x09:  # 異常回報確認訊息
            pass
            # sendbuf = self.handleAbnormalReportUpdateUplink(TTIAHeaderdata, data)
        elif message_id == 0x0C:  # 華夏自定義的protocol，處理站牌名稱
            pass
            # sendbuf = self.handleStopNameMsgTagUplink(TTIAHeaderdata, data)
            return
        else:
            raise NotImplementedError("no message payload define.")

    @classmethod
    def default_create_payload_obj(cls, message_id):
        if message_id == 0x00:  # 註冊請求訊息
            return RegUplink(init_data=b'', init_type='default')
        elif message_id == 0x01:  # 基本資料設定確認訊息
            return RegDownlink(init_data=b'', init_type='default')
        elif message_id == 0x02:  # 基本資料設定確認訊息
            return ReportBaseMsgTagUplink(init_data=b'', init_type='default')
        elif message_id == 0x03:  # 定時回報確認訊息
            return ReportMsgcountUplink(init_data=b'', init_type='default')
        elif message_id == 0x04:  # 定時回報確認訊息
            return ReportMsgcountDownlink(init_data=b'', init_type='default')
        elif message_id == 0x05:  # 定時回報確認訊息
            return ReportUpdateMsgTagDownlink(init_data=b'', init_type='default')
        elif message_id == 0x06:  # 更新站牌文字確認訊息
            return ReportUpdateMsgTagUplink(init_data=b'', init_type='default')
        elif message_id == 0x07:  # 更新站牌文字確認訊息
            return ReportUpdateBusinfoDownlink(init_data=b'', init_type='default')
        elif message_id == 0x08:  # 更新即時公車資訊確認訊息
            return

        elif message_id == 0x09:  # 異常回報確認訊息
            return

        elif message_id == 0x0C:  # 華夏自定義的protocol，處理站牌名稱
            return

    @classmethod
    def json_create_payload_obj(cls, payload_json, message_id):
        if message_id == 0x00:  # 註冊請求訊息
            return RegUplink(init_data=payload_json, init_type='json')
        elif message_id == 0x01:  # 基本資料設定確認訊息
            return RegDownlink(init_data=payload_json, init_type='json')
        elif message_id == 0x02:  # 基本資料設定確認訊息
            return ReportBaseMsgTagUplink(init_data=payload_json, init_type='json')
        elif message_id == 0x03:  # 定時回報確認訊息
            return ReportMsgcountUplink(init_data=payload_json, init_type='json')
        elif message_id == 0x04:  # 定時回報確認訊息
            return ReportMsgcountDownlink(init_data=payload_json, init_type='json')
        elif message_id == 0x05:  # 定時回報確認訊息
            return ReportUpdateMsgTagDownlink(init_data=payload_json, init_type='json')
        elif message_id == 0x06:  # 更新站牌文字確認訊息
            return ReportUpdateMsgTagUplink(init_data=payload_json, init_type='json')
        elif message_id == 0x07:  # 更新站牌文字確認訊息
            return ReportUpdateBusinfoDownlink(init_data=payload_json, init_type='json')
        elif message_id == 0x08:  # 更新即時公車資訊確認訊息
            return

        elif message_id == 0x09:  # 異常回報確認訊息
            return

        elif message_id == 0x0C:  # 華夏自定義的protocol，處理站牌名稱
            return
