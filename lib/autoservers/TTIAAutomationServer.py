from lib.udp_server.ttiastopudpserver import TTIAStopUdpServer
from .TTIAAutoMsgServer import TTIAAutoMsgServer
from .TTIAAutoBusInfoServer import TTIAAutoBusInfoServer
from .TTIAAutoStopAndRouteServer import TTIAAutoStopAndRouteServer
from lib.db_control import EStopObjCacher, MsgCacher, BusInfoCacher

import logging

logger = logging.getLogger(__name__)


class TTIAAutomationServer:
    def __init__(self, sql_config, udp_server: TTIAStopUdpServer):
        self.udp_server = udp_server
        EStopObjCacher(sql_config).load_from_sql()
        MsgCacher(sql_config).load_from_sql()
        BusInfoCacher().load_from_web()

        self.TTIAAutoStopandRouteServer = TTIAAutoStopAndRouteServer(self.udp_server)
        self.TTIAAutoMsgServer = TTIAAutoMsgServer(self.udp_server)
        self.TTIAAutoBusInfoServer = TTIAAutoBusInfoServer(self.udp_server)
