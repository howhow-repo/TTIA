import struct
from .test_base_case import TestBaseCase
from lib.TTIA_stop_message import MessageConstants

MESSAGEID = 0x00
CustomerID = 65535
CarID = 'AB-123'
DriverID = 'DV-123'
IDStorage = 1
Reserved = 0


payload = struct.pack('<15s15sBBBB',
                         bytearray(IMSI.encode('ascii')),
                         bytearray(IMEI.encode('ascii')),
                         FV1, FV2, FV3, Reserved)


HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         CustomerID,
                         CarID,
                         1,
                         DriverID,
                         65535,  # Sequence
                         Reserved,
                         len(payload))  # Len

pdu_pack = HEADER_PDU + payload


class TestREGUPLINK(TestBaseCase):
    pdu_pack = pdu_pack
    MESSAGEID = MESSAGEID


if __name__ == '__main__':
    pass
