import struct

from lib.TTIA_stop_message import TTIABusStopMessage, MessageConstants

MESSAGEID = 0x00
Provider = 65535
HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         34)  # Len

IMSI = 'IMSI123456'
IMEI = 'IMEI7891'
FV1, FV2, FV3 = 5, 0, 1
Reserved = 0
REGUPLINK_PDU = HEADER_PDU + struct.pack('<15s15sBBBB',
                                         bytearray(IMSI.encode('ascii')),
                                         bytearray(IMEI.encode('ascii')),
                                         FV1, FV2, FV3, Reserved)


class TestREGUPLINK:
    def __init__(self):
        REGUPLINK = TTIABusStopMessage(init_data=REGUPLINK_PDU, init_type='pdu')
        print((REGUPLINK.to_pdu()))
        print(REGUPLINK_PDU)
        print(REGUPLINK.to_pdu() == REGUPLINK_PDU, "\n")
