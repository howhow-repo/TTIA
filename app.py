import atexit
from apscheduler.triggers.cron import CronTrigger
from decouple import config
from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from swagger_page_context import SWAGGER_CONTEXT, SWAGGER_CONFIG
from apscheduler.schedulers.background import BackgroundScheduler

from lib import EStopObjCacher


TIMEZONE = "Asia/Taipei"

sql_config = {
    "host": config('SQL_HOST'),
    "port": int(config('SQL_PORT')),
    "user": config('SQL_USER'),
    "password": config('SQL_PW'),
    "db": config('SQL_DB')
}

app = Flask(__name__)
app.config['SWAGGER'] = SWAGGER_CONFIG
swagger = Swagger(app,template=SWAGGER_CONTEXT)

estop_cacher = EStopObjCacher(sql_config)
estop_cacher.load_from_sql()

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


@app.route("/", methods=['GET'])
def redirect_to_apidocs():
    return redirect("/docs")


@app.route("/stopapi/v1/get_cache", methods=['GET'])
def get_all_cache():
    """get all e stop current info in json.
    ---
    responses:
      200:
        description: Return the current cache of estops
    """
    r = {}
    for es in estop_cacher.estop_cache:
        r[es] = estop_cacher.estop_cache[es].to_dict()
    return jsonify(r)


@app.route("/stopapi/v1/get_cache/<stop_id>", methods=['GET'])
def get_cache_by_id(stop_id):
    """get specific e stop current info in json by stop id.
    ---
    parameters:
      - name: stop_id
        in: path
        type: integer
        required: true
        default: 1
    responses:
      200:
        description: Return the current cache of estop id
    """
    return jsonify(estop_cacher.estop_cache[int(stop_id)].to_dict())


class OperationResponse:
    def __init__(self, resault: str = 'success', error_code: int = 0, message: str = ''):
        r = {
            'resault': resault,
            'error_code': error_code,
            'message': message,
        }
        if r['message'] == '':
            del r['message']
        self.response = r


@app.route("/stopapi/v1/operate/", methods=['POST'])
def do_operation():
    """Force chche to reload from mysql.
    ---
    parameters:
      - name: action
        in: body
        type: string
        required: true
        schema:
          id: operate
          type: object
          required:
            - action
          properties:
            action:
              type: string
              description: force_reload_estop or reload_estop_by_id or estop_reboot
            ids:
              type: array
              description: stop ids.
              items:
                type: integer
                required: false
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()

    if post_body['action'] == "force_reload_estop":
        try:
            estop_cacher.load_from_sql()
        except Exception as err:
            return jsonify(OperationResponse(resault="fail",
                                             error_code=2,
                                             message=f"fail reload estop, {err}").response)

    elif post_body['action'] == "force_reload_estop":
        try:
            estop_cacher.load_from_sql_by_estop_ids(post_body['ids'])
        except Exception as err:
            return jsonify(OperationResponse(resault="fail",
                                             error_code=2,
                                             message=f"fail reload estop of {post_body['ids']}, {err}").response)

    elif post_body['action'] == "estop_reboot":
        try:
            raise NotImplementedError
        except Exception as err:
            return jsonify(OperationResponse(resault="fail",
                                             error_code=2,
                                             message=f"fail rebooting estop of {post_body['ids']}, {err}").response)

    else:
        return jsonify(OperationResponse(resault="fail",
                                         error_code=1,
                                         message=f"No that kind of action.").response)

    return jsonify(OperationResponse().response)


if __name__ == '__main__':
    """
        WARNING! Please keep the use_reloader=False
        using use_reloader may cause unknown bug in BackgroundScheduler.
        (every task will execute twice with no reason.)
        (check https://stackify.dev/288431-apscheduler-in-flask-executes-twice)
    """
    app.run(use_reloader=False, debug=True)
