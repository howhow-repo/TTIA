import atexit
from apscheduler.triggers.cron import CronTrigger
from decouple import config
from flask import Flask, redirect
from flasgger import Swagger
from swagger_page_context import SWAGGER_CONTEXT, SWAGGER_CONFIG
from apscheduler.schedulers.background import BackgroundScheduler

from lib import EStopObjCacher
from views.api import flasgger_page

TIMEZONE = config('TIMEZONE', default="Asia/Taipei")
SQL_CONFIG = {
    "host": config('SQL_HOST'),
    "port": int(config('SQL_PORT')),
    "user": config('SQL_USER'),
    "password": config('SQL_PW'),
    "db": config('SQL_DB')
}

#  init cacher
estop_cacher = EStopObjCacher(SQL_CONFIG)
estop_cacher.load_from_sql()

#  init scheduler
scheduler = BackgroundScheduler(timezone=TIMEZONE)
scheduler.add_job(func=estop_cacher.load_from_sql,
                  trigger=CronTrigger(
                      hour="00",
                      minute="01",
                      timezone=TIMEZONE
                  ),
                  id='cache_daily_reload',
                  max_instances=1,
                  replace_existing=True,)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

#  init http server
app = Flask(__name__)
app.config['SWAGGER'] = SWAGGER_CONFIG
swagger = Swagger(app, template=SWAGGER_CONTEXT)
app.register_blueprint(flasgger_page)


@app.route("/", methods=['GET'])
def redirect_to_apidocs():
    return redirect("/docs")


if __name__ == '__main__':
    """
        WARNING! Please keep the use_reloader=False
        using use_reloader may cause unknown bug in BackgroundScheduler.
        (every task will execute twice with no reason.)
        (check https://stackify.dev/288431-apscheduler-in-flask-executes-twice)
    """
    app.run(use_reloader=False, debug=True)
