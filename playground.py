import struct

from lib import TTIABusStopMessage
from lib import MessageConstants
from lib.test import TestREGUPLINK, TestREGDOWNLINK, TestReportBaseMsgTagUplink, TestReportMsgcountDownlink,\
    TestReportMsgcountUplink, TestReportUpdateMsgTagDownlink, TestReportUpdateMsgTagUplink, \
    TestReportUpdateBusinfoUplink, TestReportUpdateBusinfoDownlink, TestReportAbnormalUplink

TestREGUPLINK()
TestREGDOWNLINK()
TestReportBaseMsgTagUplink()
TestReportMsgcountUplink()
TestReportMsgcountDownlink()
TestReportUpdateMsgTagDownlink()
TestReportUpdateMsgTagUplink()
TestReportUpdateBusinfoDownlink()
TestReportUpdateBusinfoUplink()
TestReportAbnormalUplink()
# t = TTIABusStopMessage(0 ,'default')
