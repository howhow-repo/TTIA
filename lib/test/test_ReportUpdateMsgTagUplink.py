import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x06
Provider = 65535

MsgTag = 0
MsgNo = 0
MsgStatus = 12
Reserved = 0

payload = struct.pack('<HHBB', MsgTag, MsgNo, MsgStatus, Reserved)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestReportUpdateMsgTagUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        def test_from_to_pdu_by_raw_pdu(self):
            msg = TTIABusStopMessage(init_data=pdu_pack, init_type='pdu')
            self.assertEqual(msg.to_pdu(), pdu_pack)

    def test_from_to_dict_by_default_creation(self):
        default_msg = TTIABusStopMessage(init_data=MESSAGEID, init_type='default')
        obj_dict = default_msg.to_dict()
        from_dict_msg = TTIABusStopMessage(init_data=obj_dict, init_type='dict')
        self.assertEqual(from_dict_msg.to_dict(), obj_dict)
