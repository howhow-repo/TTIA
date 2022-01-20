import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x11
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

ReportRebootUplink_PDU = HEADER_PDU + payload


class TestReportRebootUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportRebootUplink = TTIABusStopMessage(init_data=ReportRebootUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportRebootUplink.header.MessageID)
        print("ORG PDU:     ", ReportRebootUplink_PDU)
        print("BYPASS PDU:  ", ReportRebootUplink.to_pdu())
        print("json:        ", ReportRebootUplink.to_dict(), '\n')
        self.assertEqual( ReportRebootUplink.to_pdu(), ReportRebootUplink_PDU)
