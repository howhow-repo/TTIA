import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x0D
Provider = 65535

LightSet = 9


payload = struct.pack('<B', LightSet)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportSetBrightnessDownlink_PDU = HEADER_PDU + payload


class TestReportSetBrightnessDownlink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportSetBrightnessDownlink = TTIABusStopMessage(init_data=ReportSetBrightnessDownlink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportSetBrightnessDownlink.header.MessageID)
        print("ORG PDU:     ", ReportSetBrightnessDownlink_PDU)
        print("BYPASS PDU:  ", ReportSetBrightnessDownlink.to_pdu())
        print("json:        ", ReportSetBrightnessDownlink.to_dict(), '\n')
        self.assertEqual( ReportSetBrightnessDownlink.to_pdu(), ReportSetBrightnessDownlink_PDU)
