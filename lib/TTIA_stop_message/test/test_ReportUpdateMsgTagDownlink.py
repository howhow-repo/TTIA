import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants
from .test_base_case import TestStopMsgBaseCase


MESSAGEID = 0x05
Provider = 65535

MsgTag = 0
MsgNo = 0
MsgContent = "我是中文"

MsgPriority = 0
MsgType = 0
MsgStopDelay = 2
MsgChangeDelay = 1


payload = struct.pack('<HH160s', MsgTag, MsgNo, bytearray(MsgContent.encode("big5")))

option_payload = struct.pack('<BBBB',
                           MsgPriority,
                           MsgType,
                           MsgStopDelay,
                           MsgChangeDelay,
                           )

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload + option_payload


class TestReportUpdateMsgTagDownlink(TestStopMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID
