import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestStopMsgBaseCase


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


class TestReportUpdateGifDownlink(TestStopMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
