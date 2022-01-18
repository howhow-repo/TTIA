import struct

from lib import TTIABusStopMessage
from lib import MessageConstants
from lib.test import TestREGUPLINK, TestREGDOWNLINK, TestReportBaseMsgTagUplink

t = TestREGUPLINK()
t = TestREGDOWNLINK()
t = TestReportBaseMsgTagUplink()

# t = TTIABusStopMessage(0 ,'default')
