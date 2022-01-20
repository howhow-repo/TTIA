import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x13
Provider = 65535

payload = b''

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportUpdateGifUplink_PDU = HEADER_PDU + payload


class TestReportUpdateGifUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportUpdateGifUplink = TTIABusStopMessage(init_data=ReportUpdateGifUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportUpdateGifUplink.header.MessageID)
        print("ORG PDU:     ", ReportUpdateGifUplink)
        print("BYPASS PDU:  ", ReportUpdateGifUplink.to_pdu())
        print("json:        ", ReportUpdateGifUplink.to_dict(), '\n')
        self.assertEqual( ReportUpdateGifUplink.to_pdu(), ReportUpdateGifUplink_PDU)
