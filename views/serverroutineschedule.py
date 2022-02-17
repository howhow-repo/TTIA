from lib import EStopObjCacher, TTIAStopUdpServer, RouteCacher
from .serversideapi import estop_udp_server
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from decouple import config

TIMEZONE = config('TIMEZONE', default="Asia/Taipei")

routine_scheduler = BackgroundScheduler(timezone=TIMEZONE)

routine_scheduler.add_job(
    func=EStopObjCacher.load_from_sql,
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
    func=lambda: estop_udp_server.reload_msg,
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
    func=RouteCacher.reload_from_sql,
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
    func=TTIAStopUdpServer.expire_timeout_section,
    trigger='interval',
    id='expire_timeout_section',
    seconds=TTIAStopUdpServer.section_lifetime / 2
)

routine_scheduler.add_job(
    func=EStopObjCacher.check_online,
    trigger='interval',
    id='check_online',
    seconds=60
)
