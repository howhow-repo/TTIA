import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x09
Provider = 65535
IMSI = 'IMSI123456'
IMEI = 'IMEI7891'

StatusCode = 255
Type = 1
TransYear = 2021
TransMonth = 1
TransDay = 1
TransHour = 1
TransMinute = 0
TransSecond = 0
RcvYear = 2021
RcvMonth = 5
RcvDay = 5
RcvHour = 6
RcvMinute = 15
RcvSecond = 15

payload = struct.pack('<BBBBBBBBBBBBBB',
                           StatusCode,
                           Type,
                           TransYear - 2000,
                           TransMonth,
                           TransDay,
                           TransHour,
                           TransMinute,
                           TransSecond,
                           RcvYear - 2000,
                           RcvMonth,
                           RcvDay,
                           RcvHour,
                           RcvMinute,
                           RcvSecond)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len


pdu_pack = HEADER_PDU + payload


class TestReportAbnormalUplink(unittest.TestCase):
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
