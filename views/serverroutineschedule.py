from lib import EStopObjCacher, TTIAStopUdpServer
from .serversideapi import estop_auto_server
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from decouple import config

TIMEZONE = config('TIMEZONE', default="Asia/Taipei")

routine_scheduler = BackgroundScheduler(timezone=TIMEZONE)

routine_scheduler.add_job(
    func=estop_auto_server.TTIAAutoStopandRouteServer.reload_stop_and_route,
    trigger=CronTrigger(
        hour="00",
        minute="01",
        timezone=TIMEZONE
    ),
    id='cache_daily_reload',
    max_instances=1,
    replace_existing=True
)

routine_scheduler.add_job(
    func=estop_auto_server.TTIAAutoMsgServer.reload_msg,
    trigger=CronTrigger(
        hour="00",
        minute="05",
        timezone=TIMEZONE
    ),
    id='stop_msg_daily_reload',
    max_instances=1,
    replace_existing=True
)

routine_scheduler.add_job(
    func=estop_auto_server.TTIAAutoStopandRouteServer.reload_stop_and_route,
    trigger=CronTrigger(
        hour="00",
        minute="10",
        timezone=TIMEZONE
    ),
    id='route_info_daily_reload',
    max_instances=1,
    replace_existing=True
)

routine_scheduler.add_job(
    func=EStopObjCacher.check_online,
    trigger='interval',
    id='check_online',
    seconds=60
)

routine_scheduler.add_job(
    func=estop_auto_server.TTIAAutoBusInfoServer.reload_bus_info,
    trigger='interval',
    id='reload_bus_info',
    seconds=20
)
