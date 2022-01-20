import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x0E
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

ReportSetBrightnessUplink_PDU = HEADER_PDU + payload


class TestReportSetBrightnessUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportSetBrightnessUplink = TTIABusStopMessage(init_data=ReportSetBrightnessUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportSetBrightnessUplink.header.MessageID)
        print("ORG PDU:     ", ReportSetBrightnessUplink_PDU)
        print("BYPASS PDU:  ", ReportSetBrightnessUplink.to_pdu())
        print("json:        ", ReportSetBrightnessUplink.to_dict(), '\n')
        self.assertEqual( ReportSetBrightnessUplink.to_pdu(), ReportSetBrightnessUplink_PDU)
