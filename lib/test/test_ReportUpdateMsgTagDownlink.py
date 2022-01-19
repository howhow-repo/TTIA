import struct

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x05
Provider = 65535

MsgTag = 0
MsgNo = 0
MsgContent = "我是中文"

MsgPriority = 0
MsgType = 0
MsgStopDelay = 2
MsgChangeDelay = 1


payload = struct.pack('<HH160s', MsgTag, MsgNo, bytearray(MsgContent.encode("big5")))

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

ReportUpdateMsgTagDownlink_PDU = HEADER_PDU + payload + option_payload


class TestReportUpdateMsgTagDownlink:
    def __init__(self):
        ReportUpdateMsgTagDownlink = TTIABusStopMessage(init_data=ReportUpdateMsgTagDownlink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportUpdateMsgTagDownlink.header.MessageID)
        print("ORG PDU:     ", ReportUpdateMsgTagDownlink_PDU)
        print("BYPASS PDU:  ", ReportUpdateMsgTagDownlink.to_pdu())
        print("json:        ", ReportUpdateMsgTagDownlink.to_dict())
        print("is same: ", ReportUpdateMsgTagDownlink.to_pdu() == ReportUpdateMsgTagDownlink_PDU, "\n")
