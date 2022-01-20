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


ReportAbnormalUplink_PDU = HEADER_PDU + payload


class TestReportAbnormalUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportAbnormalUplink = TTIABusStopMessage(init_data=ReportAbnormalUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportAbnormalUplink.header.MessageID)
        print("ORG PDU:     ", ReportAbnormalUplink_PDU)
        print("BYPASS PDU:  ", ReportAbnormalUplink.to_pdu())
        print("json:        ", ReportAbnormalUplink.to_dict(), '\n')
        self.assertEqual(ReportAbnormalUplink.to_pdu(), ReportAbnormalUplink_PDU, "\n")
