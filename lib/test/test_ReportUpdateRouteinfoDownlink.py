import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x0B
Provider = 65535

RouteID = 0
PathCName = '中文站名'
PathEName = 'stop eng name'
Sequence = 0


payload = struct.pack('<H12s12sH',
                      RouteID, bytearray(PathCName.encode('big5')),
                      bytearray(PathEName.encode('ascii')),
                      Sequence)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestReportUpdateRouteinfoDownlink(unittest.TestCase):
    def test_from_to_pdu(self):
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
