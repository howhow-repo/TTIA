from flask import Blueprint, jsonify, request
from lib import EStopObjCacher

"""
    Features in swagger page 
"""

flasgger_server = Blueprint('flasgger_server', __name__)


@flasgger_server.route("/stopapi/v1/get_cache", methods=['GET'])
def get_all_cache():
    """get all e stop current info in json.
    ---
    tags:
      - name: TTIA estop
    responses:
      200:
        description: Return the current cache of estops
    """
    r = {}
    for es in EStopObjCacher.estop_cache:
        r[es] = EStopObjCacher.estop_cache[es].to_dict()
    return jsonify(r)


@flasgger_server.route("/stopapi/v1/get_cache/<stop_id>", methods=['GET'])
def get_cache_by_id(stop_id):
    """get specific e stop current info in json by stop id.
    ---
    tags:
      - name: TTIA estop
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
    return jsonify(EStopObjCacher.estop_cache[int(stop_id)].to_dict())


class OperationResponse:
    def __init__(self, result: str = 'success', error_code: int = 0, message: str = None):
        r = {
            'result': result,
            'error_code': error_code,
        }
        if message is not None:
            r['message'] = message
        self.response = r


@flasgger_server.route("/stopapi/v1/operate/", methods=['POST'])
def do_operation():
    """Force cacher to reload from mysql. See more parameter description in Models below.
    ---
    tags:
      - name: TTIA estop
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
            EStopObjCacher.load_from_sql()
        except Exception as err:
            return jsonify(OperationResponse(result="fail",
                                             error_code=2,
                                             message=f"fail reload estop, {err}").response)

    elif post_body['action'] == "reload_estop_by_id":
        try:
            EStopObjCacher.load_from_sql_by_estop_ids(post_body['ids'])
        except Exception as err:
            return jsonify(OperationResponse(result="fail",
                                             error_code=2,
                                             message=f"fail reload estop of {post_body['ids']}, {err}").response)

    elif post_body['action'] == "estop_reboot":
        try:
            raise NotImplementedError
        except Exception as err:
            return jsonify(OperationResponse(result="fail",
                                             error_code=2,
                                             message=f"fail rebooting estop of {post_body['ids']}, {err}").response)

    else:
        return jsonify(OperationResponse(result="fail",
                                         error_code=1,
                                         message=f"No that kind of action.").response)

    return jsonify(OperationResponse().response)