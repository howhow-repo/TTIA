import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x12
Provider = 65535

PicNo = 3
PicNum = 4
PicURL = 'http://123.456.789'
MsgContent = '訊息內容 獨立式站牌: 動態圖示[A_序號_日 期版本] 範例:端午 動態圖示 [A_03_20190501] 三排式站牌: 動態圖示[B_序號_日 期版本] 範例:端午 動態圖示 [B_03_20190501] (和 MessageID=0x05 進行對應)'

payload = struct.pack("<HH160s160s", PicNo, PicNum,
                           bytearray(PicURL.encode('ascii')),
                           bytearray(MsgContent.encode('big5'))
                           )

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestReportUpdateGifDownlink(unittest.TestCase):
    def test_from_to_pdu_by_raw_pdu(self):
        msg = TTIABusStopMessage(init_data=pdu_pack, init_type='pdu')
        self.assertEqual(msg.to_pdu(), pdu_pack)

    def test_from_to_dict_by_default_creation(self):
        default_msg = TTIABusStopMessage(init_data=MESSAGEID, init_type='default')
        obj_dict = default_msg.to_dict()
        from_dict_msg = TTIABusStopMessage(init_data=obj_dict, init_type='dict')
        self.assertEqual(from_dict_msg.to_dict(), obj_dict)

    def test_from_to_pdu_by_default_creation(self):
        default_msg = TTIABusStopMessage(init_data=MESSAGEID, init_type='default')
        msg = TTIABusStopMessage(init_data=default_msg.to_pdu(), init_type='pdu')
        self.assertEqual(msg.to_pdu(), default_msg.to_pdu())
        self.assertEqual(msg.to_dict(), default_msg.to_dict())
