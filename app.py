import atexit
import threading
import logging

from apscheduler.triggers.cron import CronTrigger
from decouple import config
from flask import Flask
from flasgger import Swagger
from swagger_page_context import SWAGGER_CONTEXT, SWAGGER_CONFIG
from apscheduler.schedulers.background import BackgroundScheduler

from lib import EStopObjCacher, TTIAStopUdpServer
from views.api import flasgger_page
from views.index import index_pade


#  init constants

logger = logging.getLogger(__name__)
TIMEZONE = config('TIMEZONE', default="Asia/Taipei")
TTIA_UDP_PORT = config('TTIA_UDP_PORT', cast=int, default=50000)
SQL_CONFIG = {
    "host": config('SQL_HOST'),
    "port": config('SQL_PORT', cast=int),
    "user": config('SQL_USER'),
    "password": config('SQL_PW'),
    "db": config('SQL_DB')
}


#  init cacher
EStopObjCacher(SQL_CONFIG).load_from_sql()


#  init scheduler
scheduler = BackgroundScheduler(timezone=TIMEZONE)
scheduler.add_job(func=EStopObjCacher.load_from_sql,
                  trigger=CronTrigger(
                      hour="00",
                      minute="01",
                      timezone=TIMEZONE
                  ),
                  id='cache_daily_reload',
                  max_instances=1,
                  replace_existing=True,)

scheduler.add_job(func=TTIAStopUdpServer.expire_timeout_section,
                  trigger='interval',
                  id='expire_timeout_section',
                  seconds=TTIAStopUdpServer.section_lifetime/2)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


#  init flask server
app = Flask(__name__)
app.config['SWAGGER'] = SWAGGER_CONFIG
swagger = Swagger(app, template=SWAGGER_CONTEXT)
app.register_blueprint(index_pade)
app.register_blueprint(flasgger_page)


#  init http server
estop_udp_server = TTIAStopUdpServer(host="localhost", port=TTIA_UDP_PORT, )


if __name__ == '__main__':
    """
        WARNING! Please keep the use_reloader=False
        using use_reloader may cause unknown bug in BackgroundScheduler.
        (every task will execute twice with no reason.)
        (check https://stackify.dev/288431-apscheduler-in-flask-executes-twice)
    """
    logging.basicConfig(filename='myapp.log', level=logging.DEBUG)
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    http_thread = threading.Thread(target=lambda: app.run(use_reloader=False, debug=True)).start()
    udp_thread = threading.Thread(target=estop_udp_server.start()).start()
