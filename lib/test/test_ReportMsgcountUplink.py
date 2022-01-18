import struct

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x03
Provider = 65535

SentCount = 0
RecvCount = 0

payload = struct.pack('<HH',
                        SentCount,
                        RecvCount
                      )

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportMsgcountUplink_PDU = HEADER_PDU + payload


class TestReportMsgcountUplink:
    def __init__(self):
        ReportMsgcountUplink = TTIABusStopMessage(init_data=ReportMsgcountUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportMsgcountUplink.header.MessageID)
        print((ReportMsgcountUplink.to_pdu()))
        print(ReportMsgcountUplink_PDU)
        print(ReportMsgcountUplink.to_pdu() == ReportMsgcountUplink_PDU, "\n")