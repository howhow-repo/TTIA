import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x08
Provider = 65535

MsgStatus = 0
Reserved = 0

payload = struct.pack('<BB', MsgStatus, Reserved)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportUpdateBusinfoUplink_PDU = HEADER_PDU + payload


class TestReportUpdateBusinfoUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportUpdateBusinfoUplink = TTIABusStopMessage(init_data=ReportUpdateBusinfoUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportUpdateBusinfoUplink.header.MessageID)
        print("ORG PDU:     ", ReportUpdateBusinfoUplink_PDU)
        print("BYPASS PDU:  ", ReportUpdateBusinfoUplink.to_pdu())
        print("json:        ", ReportUpdateBusinfoUplink.to_dict(), '\n')
        self.assertEqual( ReportUpdateBusinfoUplink.to_pdu(), ReportUpdateBusinfoUplink_PDU)
