import struct

from lib import TTIABusStopMessage, MessageConstants


HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         0x0E,
                         1234,
                         65535,  # StopID
                         65535,  # Sequence
                         0)  # Len

# I need to decode coming udp binary message:
coming_binary = HEADER_PDU
msg = TTIABusStopMessage(init_data=coming_binary, init_type='pdu')

print(msg.to_dict())  # you can check data by printing out .to_dict
print(msg.payload.to_dict())  # or check directly by to properties

# I need a empty msg for responding:
