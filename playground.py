import struct

from lib import TTIABusStopMessage
from lib import MessageConstants
from lib.test import TestREGUPLINK, TestREGDOWNLINK, TestReportBaseMsgTagUplink, \
    TestReportMsgcountUplink, TestReportUpdateMsgTagDownlink, TestReportUpdateMsgTagUplink

TestREGUPLINK()
TestREGDOWNLINK()
TestReportBaseMsgTagUplink()
TestReportMsgcountUplink()
TestReportUpdateMsgTagDownlink()
TestReportUpdateMsgTagUplink()
TestReportUpdateMsgTagDownlink()
# t = TTIABusStopMessage(0 ,'default')
