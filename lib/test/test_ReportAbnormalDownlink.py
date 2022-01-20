import struct
import unittest

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x0A
Provider = 65535
IMSI = 'IMSI123456'
IMEI = 'IMEI7891'

MsgStatus = 1
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

ReportAbnormalDownlink_PDU = HEADER_PDU + payload


class TestReportAbnormalDownlink(unittest.TestCase):
    def test_from_to_pdu(self):
        ReportAbnormalDownlink = TTIABusStopMessage(init_data=ReportAbnormalDownlink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportAbnormalDownlink.header.MessageID)
        print("ORG PDU:     ", ReportAbnormalDownlink_PDU)
        print("BYPASS PDU:  ", ReportAbnormalDownlink.to_pdu())
        print("json:        ", ReportAbnormalDownlink.to_dict(), '\n')
        self.assertEqual( ReportAbnormalDownlink.to_pdu(), ReportAbnormalDownlink_PDU)
