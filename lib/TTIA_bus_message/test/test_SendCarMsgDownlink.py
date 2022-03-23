import struct
import unittest
from .test_base_case import TestBusMsgBaseCase
from lib.TTIA_bus_message import MessageConstants

# header para
MESSAGEID = 0x06
CustomerID = 65535
CarID = 60000
head_DriverID = 123456
IDStorage = 1
head_Reserved = 0

# payload para
Action = 0
InfoID = 0
Reserved = 0
Information = '內容內容內容內容'

context = Information.encode('big5')

payload_pdu = struct.pack(f'<BHB{len(context)}s', Action, InfoID, Reserved, context)

HEADER_PDU = struct.pack(
    '<4sBBHHBIHBH',
    bytearray(MessageConstants.ProtocolID.encode('ascii')),
    MessageConstants.ProtocolVer,
    MESSAGEID,
    CustomerID,
    CarID,
    1,
    head_DriverID,
    65535,  # Sequence
    head_Reserved,
    len(payload_pdu)  # Len
)

pdu_pack = HEADER_PDU + payload_pdu


class TestSendCarMsgDownlink(TestBusMsgBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    unittest.main()
