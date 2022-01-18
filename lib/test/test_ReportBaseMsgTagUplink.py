import struct

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x02
Provider = 65535
HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         4)  # Len

MsgTag = 0
MsgStatus = 0
Reserved = 0
ReportBaseMsgTagUplink_PDU = HEADER_PDU + struct.pack('<HBB',
                                         MsgTag,
                                         MsgStatus,
                                         Reserved)


class TestReportBaseMsgTagUplink:
    def __init__(self):
        ReportBaseMsgTagUplink = TTIABusStopMessage(init_data=ReportBaseMsgTagUplink_PDU, init_type='pdu')
        print((ReportBaseMsgTagUplink.to_pdu()))
        print(ReportBaseMsgTagUplink_PDU)
        print(ReportBaseMsgTagUplink.to_pdu() == ReportBaseMsgTagUplink_PDU, "\n")