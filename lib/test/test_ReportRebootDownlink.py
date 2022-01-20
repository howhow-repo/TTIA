import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x10
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

ReportRebootDownlink_PDU = HEADER_PDU + payload


class TestReportRebootDownlink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportRebootDownlink = TTIABusStopMessage(init_data=ReportRebootDownlink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportRebootDownlink.header.MessageID)
        print("ORG PDU:     ", ReportRebootDownlink_PDU)
        print("BYPASS PDU:  ", ReportRebootDownlink.to_pdu())
        print("json:        ", ReportRebootDownlink.to_dict(), '\n')
        self.assertEqual( ReportRebootDownlink.to_pdu(), ReportRebootDownlink_PDU)
