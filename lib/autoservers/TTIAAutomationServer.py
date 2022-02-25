from decouple import config
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from ..udp_server.ttiastopudpserver import TTIAStopUdpServer
from .TTIAAutoMsgServer import TTIAAutoMsgServer
from .TTIAAutoBusInfoServer import TTIAAutoBusInfoServer
from .TTIAAutoStopAndRouteServer import TTIAAutoStopAndRouteServer
from ..db_control import EStopObjCacher, MsgCacher, BusInfoCacher

import logging

logger = logging.getLogger(__name__)
TIMEZONE = config('TIMEZONE', default="Asia/Taipei")


class TTIAAutomationServer:
    def __init__(self, sql_config: dict, udp_server: TTIAStopUdpServer):
        self.udp_server = udp_server

        self.TTIAAutoStopandRouteServer = TTIAAutoStopAndRouteServer(sql_config, self.udp_server)
        self.TTIAAutoMsgServer = TTIAAutoMsgServer(sql_config, self.udp_server)
        self.TTIAAutoBusInfoServer = TTIAAutoBusInfoServer(self.udp_server)

        self.routine_scheduler = BackgroundScheduler(timezone=TIMEZONE)
        self.set_routine_jobs()

    def set_routine_jobs(self):
        self.routine_scheduler.add_job(
            func=self.TTIAAutoStopandRouteServer.reload_stop_and_route,
            trigger=CronTrigger(
                hour="00",
                minute="01",
                timezone=TIMEZONE
            ),
            id='cache_daily_reload',
            max_instances=1,
            replace_existing=True
        )

        self.routine_scheduler.add_job(
            func=self.TTIAAutoMsgServer.reload_msg,
            trigger=CronTrigger(
                hour="00",
                minute="05",
                timezone=TIMEZONE
            ),
            id='stop_msg_daily_reload',
            max_instances=1,
            replace_existing=True
        )

        self.routine_scheduler.add_job(
            func=self.TTIAAutoStopandRouteServer.reload_stop_and_route,
            trigger=CronTrigger(
                hour="00",
                minute="10",
                timezone=TIMEZONE
            ),
            id='route_info_daily_reload',
            max_instances=1,
            replace_existing=True
        )

        self.routine_scheduler.add_job(
            func=self.TTIAAutoStopandRouteServer.check_online,
            trigger='interval',
            id='check_online',
            seconds=60
        )

        self.routine_scheduler.add_job(
            func=self.TTIAAutoBusInfoServer.reload_bus_info,
            trigger='interval',
            id='reload_bus_info',
            seconds=20
        )
