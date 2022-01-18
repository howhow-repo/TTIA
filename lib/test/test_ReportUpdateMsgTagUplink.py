import struct

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x06
Provider = 65535

MsgTag = 0
MsgNo = 0
MsgStatus = 12
Reserved = 0

payload = struct.pack('<HHBB', MsgTag, MsgNo, MsgStatus, Reserved)

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

ReportUpdateMsgTagUplink_PDU = HEADER_PDU + payload


class TestReportUpdateMsgTagUplink:
    def __init__(self):
        ReportUpdateMsgTagUplink = TTIABusStopMessage(init_data=ReportUpdateMsgTagUplink_PDU, init_type='pdu')
        print('Testing on message id: ', ReportUpdateMsgTagUplink.header.MessageID)
        print("ORG PDU:     ", ReportUpdateMsgTagUplink_PDU)
        print("BYPASS PDU:  ", ReportUpdateMsgTagUplink.to_pdu())
        print("json:        ", ReportUpdateMsgTagUplink.to_json())
        print("is same: ", ReportUpdateMsgTagUplink.to_pdu() == ReportUpdateMsgTagUplink_PDU, "\n")
