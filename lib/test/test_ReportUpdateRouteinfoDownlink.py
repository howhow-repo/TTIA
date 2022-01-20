import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x0B
Provider = 65535

RouteID = 0
PathCName = '中文站名'
PathEName = 'stop eng name'
Sequence = 0


payload = struct.pack('<H12s12sH',
                      RouteID, bytearray(PathCName.encode('big5')),
                      bytearray(PathEName.encode('ascii')),
                      Sequence)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportUpdateRouteinfoDownlink_PDU = HEADER_PDU + payload


class TestReportUpdateRouteinfoDownlink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportUpdateRouteinfoDownlink = TTIABusStopMessage(init_data=ReportUpdateRouteinfoDownlink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportUpdateRouteinfoDownlink.header.MessageID)
        print("ORG PDU:     ", ReportUpdateRouteinfoDownlink_PDU)
        print("BYPASS PDU:  ", ReportUpdateRouteinfoDownlink.to_pdu())
        print("json:        ", ReportUpdateRouteinfoDownlink.to_dict(), '\n')
        self.assertEqual( ReportUpdateRouteinfoDownlink.to_pdu(), ReportUpdateRouteinfoDownlink_PDU)
