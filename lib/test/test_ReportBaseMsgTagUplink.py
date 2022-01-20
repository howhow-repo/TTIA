import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x02
Provider = 65535
MsgTag = 0
MsgStatus = 0
Reserved = 0

payload = struct.pack('<HBB',
                        MsgTag,
                        MsgStatus,
                        Reserved)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportBaseMsgTagUplink_PDU = HEADER_PDU + payload


class TestReportBaseMsgTagUplink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportBaseMsgTagUplink = TTIABusStopMessage(init_data=ReportBaseMsgTagUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportBaseMsgTagUplink.header.MessageID)
        print("ORG PDU:     ", ReportBaseMsgTagUplink_PDU)
        print("BYPASS PDU:  ", ReportBaseMsgTagUplink.to_pdu())
        print("json:        ", ReportBaseMsgTagUplink.to_dict(), '\n')
        self.assertEqual( ReportBaseMsgTagUplink.to_pdu(), ReportBaseMsgTagUplink_PDU)
