import struct

from lib import MessageConstants, TTIABusStopMessage

Result = 0
MsgTag = 0  # 系統訊息
StopCName = '中文站名'
StopEName = 'English Stop name'
LongitudeDu = 0
LongitudeFen = 0
LongitudeMiao = 0
LatitudeDu = 0
LatitudeFen = 0
LatitudeMiao = 0
TypeID = 0
BootTimeh = 0
BootTimem = 0
BootTimes = 0
ShutdownTimeh = 0
ShutdownTimem = 0
ShutdownTimes = 0
MessageGroupID = 0
IdleMessage = ''
Year = 2022
Month = 0
Day = 0
Hour = 0
Minute = 0
Second = 0
DisplayMode = 0
TextRollingSpeed = 0
DistanceFunctionMode = 0
ReportPeriod = 0

StopCName = bytearray(StopCName.encode("big5"))
StopEName = bytearray(StopEName.encode("big5"))
IdleMessage = bytearray(IdleMessage.encode("big5"))

payload = struct.pack('<BH32s32sBBHBBHHBBBBBBB32sBBBBBBBBBH',
                      Result,
                      MsgTag,
                      StopCName,
                      StopEName,
                      LongitudeDu,
                      LongitudeFen,
                      LongitudeMiao,
                      LatitudeDu,
                      LatitudeFen,
                      LatitudeMiao,
                      TypeID,
                      BootTimeh, BootTimem, BootTimes,
                      ShutdownTimeh, ShutdownTimem, ShutdownTimes,
                      MessageGroupID,
                      IdleMessage,
                      (Year - 2000), Month, Day, Hour, Minute, Second,
                      DisplayMode, TextRollingSpeed, DistanceFunctionMode,
                      ReportPeriod )

MESSAGEID = 0x01
Provider = 65535
HEADER_PDU = struct.pack('<4sBBHQHH',
                         bytearray(MessageConstants.ProtocolID.encode('ascii')),
                         MessageConstants.ProtocolVer,
                         MESSAGEID,
                         Provider,
                         65535,  # StopID
                         65535,  # Sequence
                         len(payload))  # Len

REGDOWNLINK_PDU = HEADER_PDU + payload


class TestREGDOWNLINK:
    def __init__(self):
        REGDOWNLINK = TTIABusStopMessage(init_data=REGDOWNLINK_PDU, init_type='pdu')
        print('Testing on message id: ', REGDOWNLINK.header.MessageID)
        print((REGDOWNLINK.to_pdu()))
        print(REGDOWNLINK_PDU)
        print(REGDOWNLINK.to_pdu() == REGDOWNLINK_PDU, "\n")
