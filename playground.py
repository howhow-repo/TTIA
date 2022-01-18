import struct

from lib import TTIABusStopMessage
from lib import MessageConstants
from lib.test import TestREGUPLINK, TestREGDOWNLINK, TestReportBaseMsgTagUplink, \
    TestReportMsgcountUplink, TestReportUpdateMsgTagDownlink

TestREGUPLINK()
TestREGDOWNLINK()
TestReportBaseMsgTagUplink()
TestReportMsgcountUplink()
TestReportUpdateMsgTagDownlink()
# t = TTIABusStopMessage(0 ,'default')
