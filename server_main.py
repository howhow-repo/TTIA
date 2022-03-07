import atexit
import threading
import logging
from logging.handlers import RotatingFileHandler

#  Warning! This is weird, but i can only get the logger work by putting the code here before other import.
formatter = '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
fh = RotatingFileHandler('logs/server.log', maxBytes=1024*1024*4, backupCount=2)
fh.setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format=formatter,
                    handlers=[
                        fh,
                        logging.StreamHandler()
                    ])

from decouple import config
from flask import Flask
from flasgger import Swagger
from swagger_page_context import SWAGGER_CONTEXT, SWAGGER_CONFIG

from views.serversideapi import flasgger_server, estop_auto_server
from views.msgschedulerapi import scheduler_api
from views.index import index_pade

logger = logging.getLogger(__name__)

#  init constants
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

#  start routine_scheduler
estop_auto_server.routine_scheduler.start()
atexit.register(lambda: estop_auto_server.routine_scheduler.shutdown())

#  start msg_scheduler
estop_auto_server.TTIAAutoMsgServer.scheduler.start()
atexit.register(lambda: estop_auto_server.TTIAAutoMsgServer.scheduler.shutdown())

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

    udp_thread = threading.Thread(target=estop_auto_server.udp_server.start()).start()
