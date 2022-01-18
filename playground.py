import struct

from lib import TTIABusStopMessage
from lib import MessageConstants
from lib.test import TestREGUPLINK, TestREGDOWNLINK, TestReportBaseMsgTagUplink, \
    TestReportMsgcountUplink, TestReportUpdateMsgTagDownlink, TestReportUpdateMsgTagUplink, \
    TestReportUpdateBusinfoUplink, TestReportUpdateBusinfoDownlink

TestREGUPLINK()
TestREGDOWNLINK()
TestReportBaseMsgTagUplink()
TestReportMsgcountUplink()
TestReportUpdateMsgTagDownlink()
TestReportUpdateMsgTagUplink()
TestReportUpdateBusinfoDownlink()
TestReportUpdateBusinfoUplink()
# t = TTIABusStopMessage(0 ,'default')
