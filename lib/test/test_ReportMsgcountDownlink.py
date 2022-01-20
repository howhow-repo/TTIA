import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x04
Provider = 65535
IMSI = 'IMSI123456'
IMEI = 'IMEI7891'

payload = b''

option_payload = b''

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len


ReportMsgcountDownlink_PDU = HEADER_PDU + payload


class TestReportMsgcountDownlink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportMsgcountDownlink = TTIABusStopMessage(init_data=ReportMsgcountDownlink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportMsgcountDownlink.header.MessageID)
        print("ORG PDU:     ", ReportMsgcountDownlink_PDU)
        print("BYPASS PDU:  ", ReportMsgcountDownlink.to_pdu())
        print("json:        ", ReportMsgcountDownlink.to_dict(), '\n')
        self.assertEqual(ReportMsgcountDownlink.to_pdu(), ReportMsgcountDownlink_PDU)
