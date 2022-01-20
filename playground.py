import struct

from .lib import TTIABusStopMessage, MessageConstants
from .lib.TTIA_stop_message.header import Header

MESSAGEID = 0x01
Provider = 65535
payload = b''

HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

HEADER_DICT = {
    'ProtocolID': MessageConstants.ProtocolID,
    'ProtocolVer': MessageConstants.ProtocolVer,
    'MessageID': 0x01,
    'Provider': Provider,
    'StopID': 65535,
    'Sequence': 65535,
    'Len': len(payload)

}

header = Header(init_data=1, init_type='default')
