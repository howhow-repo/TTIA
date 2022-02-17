import atexit
import threading
import logging

from decouple import config
from flask import Flask
from flasgger import Swagger
from swagger_page_context import SWAGGER_CONTEXT, SWAGGER_CONFIG

from lib import EStopObjCacher, MsgCacher, RouteCacher
from views.serversideapi import flasgger_server, estop_udp_server
from views.serverroutineschedule import routine_scheduler
from views.msgschedulerapi import msg_scheduler
from views.msgschedulerapi import scheduler_api
from views.index import index_pade


#  init constants
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',)
logger = logging.getLogger(__name__)
TTIA_UDP_PORT = config('TTIA_UDP_SERVER_PORT', cast=int, default=50000)
HTTP_PORT = config('TTIA_HTTP_SERVER_PORT', cast=int, default=5000)
TIMEZONE = config('TIMEZONE', default="Asia/Taipei")
SQL_CONFIG = {
    "host": config('SQL_HOST'),
    "port": config('SQL_PORT', cast=int),
    "user": config('SQL_USER'),
    "password": config('SQL_PW'),
    "db": config('SQL_DB')
}


#  init cacher
EStopObjCacher(SQL_CONFIG).load_from_sql()

estop_udp_server.init_msg_jods()

RouteCacher(SQL_CONFIG, estop_udp_server).load_from_sql()


#  init routine_scheduler
routine_scheduler.start()
atexit.register(lambda: routine_scheduler.shutdown())

#  init msg_scheduler
msg_scheduler.start()
atexit.register(lambda: msg_scheduler.shutdown())

logging.getLogger('apscheduler').setLevel(logging.ERROR)


#  init flask server
app = Flask(__name__)
app.config['SWAGGER'] = SWAGGER_CONFIG
swagger = Swagger(app, template=SWAGGER_CONTEXT)
app.register_blueprint(index_pade)
app.register_blueprint(flasgger_server)
app.register_blueprint(scheduler_api)


if __name__ == '__main__':
    """
        WARNING! Please keep the use_reloader=False
        using use_reloader may cause unknown bug in BackgroundScheduler.
        (every task will execute twice with no reason.)
        (check https://stackify.dev/288431-apscheduler-in-flask-executes-twice)
    """
    http_thread = threading.Thread(target=lambda: app.run(
        host="0.0.0.0",
        port=5000,
        use_reloader=False,
        debug=True)).start()

    udp_thread = threading.Thread(target=estop_udp_server.start()).start()
