from flask import Blueprint, jsonify, request
from lib import EStopObjCacher, TTIAStopUdpServer, TTIABusStopMessage
from decouple import config

"""
    Features in swagger page 
"""

flasgger_server = Blueprint('flasgger_server', __name__)

TTIA_UDP_PORT = config('TTIA_UDP_SERVER_PORT', cast=int, default=50000)
estop_udp_server = TTIAStopUdpServer(host="localhost", port=TTIA_UDP_PORT)


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
        r[es] = EStopObjCacher.estop_cache[es].to_json()
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
    print(EStopObjCacher.estop_cache[int(stop_id)].to_json())
    return jsonify(EStopObjCacher.estop_cache[int(stop_id)].to_json())


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
def reload_caches():
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


@flasgger_server.route("/stopapi/v1/set_msg/<stop_id>", methods=['POST'])
def set_msg(stop_id):
    """Force cacher to reload from mysql. See more parameter description in Models below.
    ---
    tags:
      - name: TTIA estop
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true
        default: 1
      - name: set_msg
        in: body
        type: string
        required: true
        schema:
          id: set_msg
          type: object
          required:
            - MsgTag
            - MsgNo
            - MsgContent
          properties:
            MsgTag:
              type: number
              description: 訊息標籤，控制中 心定義之訊息代碼 0:手動機制(自中心 取得所有訊息設 定，由站牌設備自行 排程) 5:自動機制(由中心 排程下送最新一筆 訊息 50:提供獨立式9字 LED站牌氣象資訊
            MsgNo:
              type: number
              description: 訊息編號
            MsgContent:
              type: string
              description: 訊息內容(big5)
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    stop_id = int(stop_id)
    estop = EStopObjCacher.get_estop_by_id(stop_id)
    if estop and estop.ready and estop.address:
        section = estop_udp_server.create_new_section(stop_id, estop.address, 0x05)
        msg = TTIABusStopMessage(0x05, 'default')
        msg.header.StopID = stop_id
        msg.payload.from_dict(post_body)
        estop_udp_server.send_update_msg_tag(msg_obj=msg, section=section)

    elif not estop:
        return jsonify(OperationResponse(result="fail",
                                         error_code=2,
                                         message=f"estop id {stop_id} is not found in cache.").response)
    elif not estop.ready:
        return jsonify(OperationResponse(result="fail",
                                         error_code=2,
                                         message=f"estop id {stop_id} is not ready yet.").response)
    elif not estop.address:
        return jsonify(OperationResponse(result="fail",
                                         error_code=2,
                                         message=f"can not find addr of estop id {stop_id}.").response)

    return jsonify(OperationResponse().response)
