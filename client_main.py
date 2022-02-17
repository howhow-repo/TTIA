import atexit
import threading
import logging

from decouple import config
from datetime import datetime, timedelta
from flask import Flask
from flasgger import Swagger
from swagger_page_context import SWAGGER_CONTEXT, SWAGGER_CONFIG
from apscheduler.schedulers.background import BackgroundScheduler

from views.clientsideapi import flasgger_client, estop_udp_server
from views.index import index_pade

#  init constants

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')
TIMEZONE = config('TIMEZONE', default="Asia/Taipei")
TTIA_UDP_PORT = config('TTIA_UDP_CLIENT_PORT', cast=int, default=50000)
HTTP_PORT = config('TTIA_HTTP_CLIENT_PORT', cast=int, default=5000)

#  init estop
#  init in views/clientsideapi.py

# init scheduler
scheduler = BackgroundScheduler(timezone=TIMEZONE)
scheduler.add_job(func=estop_udp_server.send_period_report,
                  id='send_period_report',
                  trigger='interval',
                  seconds=estop_udp_server.estop.ReportPeriod,
                  replace_existing=True, )

scheduler.add_job(func=estop_udp_server.send_registration,
                  id='registrate_estop',
                  next_run_time=datetime.now() + timedelta(seconds=3),
                  max_instances=1, )

scheduler.start()
atexit.register(lambda: scheduler.shutdown())
logging.getLogger('apscheduler').setLevel(logging.ERROR)

#  init flask server
app = Flask(__name__)
app.config['SWAGGER'] = SWAGGER_CONFIG
swagger = Swagger(app, template=SWAGGER_CONTEXT)
app.register_blueprint(index_pade)
app.register_blueprint(flasgger_client)

if __name__ == '__main__':
    """
        WARNING! Please keep the use_reloader=False
        using use_reloader may cause unknown bug in BackgroundScheduler.
        (every task will execute twice with no reason.)
        (check https://stackify.dev/288431-apscheduler-in-flask-executes-twice)
    """
    http_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=HTTP_PORT, use_reloader=False, debug=True)).start()
    udp_thread = threading.Thread(target=estop_udp_server.start()).start()
