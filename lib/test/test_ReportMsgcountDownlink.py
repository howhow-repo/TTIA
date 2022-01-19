import struct

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x04
Provider = 65535
IMSI = 'IMSI123456'
IMEI = 'IMEI7891'

StatusCode = 255
Type = 1
TransYear = 2021
TransMonth = 1
TransDay = 1
TransHour = 1
TransMinute = 0
TransSecond = 0
RcvYear = 2021
RcvMonth = 5
RcvDay = 5
RcvHour = 6
RcvMinute = 15
RcvSecond = 15

MsgPriority = 0
MsgType = 0
MsgStopDelay = 2
MsgChangeDelay = 1

payload = struct.pack('<BBBBBBBBBBBBBB',
                           StatusCode,
                           Type,
                           TransYear - 2000,
                           TransMonth,
                           TransDay,
                           TransHour,
                           TransMinute,
                           TransSecond,
                           RcvYear - 2000,
                           RcvMonth,
                           RcvDay,
                           RcvHour,
                           RcvMinute,
                           RcvSecond)

option_payload = struct.pack('<BBBB',
                           MsgPriority,
                           MsgType,
                           MsgStopDelay,
                           MsgChangeDelay,
                           )

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len


ReportMsgcountDownlink_PDU = HEADER_PDU + payload + option_payload


class TestReportMsgcountDownlink:
    def __init__(self):
        ReportMsgcountDownlink = TTIABusStopMessage(init_data=ReportMsgcountDownlink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportMsgcountDownlink.header.MessageID)
        print("ORG PDU:     ", ReportMsgcountDownlink_PDU)
        print("BYPASS PDU:  ", ReportMsgcountDownlink.to_pdu())
        print("json:        ", ReportMsgcountDownlink.to_dict())
        print("is same: ", ReportMsgcountDownlink.to_pdu() == ReportMsgcountDownlink_PDU, "\n")
