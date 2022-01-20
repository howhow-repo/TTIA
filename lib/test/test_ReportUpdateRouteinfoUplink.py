import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x0C
Provider = 65535

MsgTag = 0
MsgStatus = 0
Reserved = 0


payload = struct.pack('<HBB', MsgTag, MsgStatus, Reserved)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportUpdateRouteinfoUplink_PDU = HEADER_PDU + payload


class TestReportUpdateRouteinfoUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportUpdateRouteinfoUplink = TTIABusStopMessage(init_data=ReportUpdateRouteinfoUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportUpdateRouteinfoUplink.header.MessageID)
        print("ORG PDU:     ", ReportUpdateRouteinfoUplink_PDU)
        print("BYPASS PDU:  ", ReportUpdateRouteinfoUplink.to_pdu())
        print("json:        ", ReportUpdateRouteinfoUplink.to_dict(), '\n')
        self.assertEqual( ReportUpdateRouteinfoUplink.to_pdu(), ReportUpdateRouteinfoUplink_PDU)
