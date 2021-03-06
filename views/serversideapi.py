import sys
from flask import Blueprint, jsonify, request
from lib import TTIABusStopMessage
from lib import EStopObjCacher, TTIAStopUdpServer, TTIAAutomationServer
from lib import FlasggerResponse
from decouple import config
import logging

"""
    Features in swagger page 
"""

logger = logging.getLogger(__name__)
flasgger_server = Blueprint('flasgger_server', __name__)

SQL_CONFIG = {
    "host": config('SQL_HOST'),
    "port": config('SQL_PORT', cast=int),
    "user": config('SQL_USER'),
    "password": config('SQL_PW'),
    "db": config('SQL_DB')
}

TTIA_UDP_PORT = config('TTIA_UDP_SERVER_PORT', cast=int, default=50000)
estop_udp_server = TTIAStopUdpServer(host="0.0.0.0", port=TTIA_UDP_PORT)
estop_auto_server = TTIAAutomationServer(sql_config=SQL_CONFIG, udp_server=estop_udp_server)


def check_stop(stop_id: int):
    estop = EStopObjCacher.get_estop_by_id(stop_id)
    if estop and estop.ready and estop.address:
        return True, "ok"
    elif not estop:
        return False, f"estop id {stop_id} is not found in cache."
    elif not estop.ready:
        return False, f"estop id {stop_id} is not ready yet."
    elif not estop.address:
        return False, f"can not find addr of estop id {stop_id}."


def create_msg(post_body, message_id: int, stop_id: int) -> TTIABusStopMessage:
    msg = TTIABusStopMessage(message_id, 'default')
    msg.header.StopID = stop_id
    msg.payload.from_dict(post_body)
    msg.option_payload.from_dict(post_body)
    return msg


@flasgger_server.route("/stopapi/v1/get_cache", methods=['GET'])
def get_all_cache():
    """get all e stop current info in json.
    ---
    tags:
      - name: TTIA EStop Server
    responses:
      200:
        description: Return the current cache of estops
    """
    r = {}
    for es in EStopObjCacher.estop_cache:
        r[es] = EStopObjCacher.estop_cache[es].to_json()
    return jsonify(r)


@flasgger_server.route("/stopapi/v1/get_cache/ready", methods=['GET'])
def get_cache_ready():
    """get estops those are ready registered.
    ---
    tags:
      - name: TTIA EStop Server
    responses:
      200:
        description: Return the current cache of estop id
    """
    estops_json = [stop_obj.to_json() for stop_obj in EStopObjCacher.estop_cache.values() if stop_obj.ready]
    return jsonify(estops_json)


@flasgger_server.route("/stopapi/v1/get_cache/<stop_id>", methods=['GET'])
def get_cache_by_id(stop_id):
    """get specific e stop current info in json by stop id.
    ---
    tags:
      - name: TTIA EStop Server
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
    estop = EStopObjCacher.get_estop_by_id(int(stop_id))
    if estop:
        return jsonify(estop.to_json())
    else:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=2,
                                        message=f"Can not find stop id {int(stop_id)}").response)


@flasgger_server.route("/stopapi/v1/reload_caches/", methods=['POST'])
def reload_caches():
    """Force cacher to reload from mysql. If route info changed, it will auto sent ttia to estop.
        See more parameter description in Models below.
    ---
    tags:
      - name: TTIA EStop Server
    parameters:
      - name: reload_caches
        in: body
        type: string
        required: true
        schema:
          id: reload_caches
          type: object
          properties:
            ids:
              type: array
              description: fill in stop ids for force refresh; keep empty to force refresh all.
              items:
                type: integer
                required: false
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    if post_body and len(post_body.get('ids')) > 0:
        # Reload by id
        try:
            estop_auto_server.TTIAAutoStopandRouteServer.reload_stop_and_route_by_ids(post_body['ids'])
            logger.info(f"estop cache reloaded by id: {post_body['ids']}")
            return jsonify(FlasggerResponse(message=f"estop cache reloaded by id: [{post_body['ids']}]").response)
        except Exception as err:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=2,
                                            message=f"fail reload estop of {post_body['ids']}, {err}").response)
    else:
        # Reload all
        # try:
        estop_auto_server.TTIAAutoStopandRouteServer.reload_stop_and_route()
        logger.info("estop cache total reloaded")
        return jsonify(FlasggerResponse(message="estop cache total reloaded").response)
    # except Exception as err:
    #     return jsonify(FlasggerResponse(result="fail",
    #                                     error_code=2,
    #                                     message=f"fail reload estop, {err}").response)


@flasgger_server.route("/stopapi/v1/set_msg/<stop_id>", methods=['POST'])
def set_msg(stop_id):
    """Update text msg to estop.
    ---
    tags:
      - name: TTIA EStop Protocol
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

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
              description: ???????????????????????? ???????????????????????? 0:????????????(????????? ????????????????????? ??????????????????????????? ??????) 5:????????????(????????? ???????????????????????? ?????? 50:???????????????9??? LED??????????????????
            MsgNo:
              type: number
              description: ????????????
            MsgContent:
              type: string
              description: ????????????(big5)
            MsgPriority:
              type: number
              description: (optional) ????????????????????? 0:?????? 1:?????? 2:??????
            MsgType:
              type: number
              description: (optional) ???????????? 0:?????? 1:?????? 2:????????????
            MsgStopDelay:
              type: number
              description: (optional) ??????:2??? ????????????????????????
              example: 2
            MsgChangeDelay:
              type: number
              description: (optional) ??????:1??? ????????????????????? ??????????????????
              example: 1
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)
    try:
        assert post_body, "post body should be in json."
        assert 'MsgTag' in post_body, "key 'MsgTag' missing"
        assert 'MsgNo' in post_body, "key 'MsgNo' missing"
        assert 'MsgContent' in post_body, "key 'MsgContent' missing"
        msg = create_msg(post_body, 0x05, int(stop_id))
        ack_msg = estop_auto_server.udp_server.send_update_msg_tag(msg_obj=msg)

        if not ack_msg:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"TimeoutError: Did not receive ack msg.").response)
        elif ack_msg.payload.MsgStatus != 1:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"OperationError: Receive fail update report.").response)
        else:
            return jsonify(FlasggerResponse(message=f"{str(ack_msg.payload.to_dict())}").response)
    except Exception as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"{e.__class__.__name__}: {e.__str__()}").response)


@flasgger_server.route("/stopapi/v1/set_bus_info/<stop_id>", methods=['POST'])
def set_bus_info(stop_id):
    """Update bus info to estop.
    ---
    tags:
      - name: TTIA EStop Protocol
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

      - name: bus_info
        in: body
        type: string
        required: true
        schema:
          id: bus_info
          type: object
          required:
            - RouteID
            - BusID
            - CurrentStop
            - DestinationStop
            - IsLastBus
            - EstimateTime
            - StopDistance
            - Direction
            - Type
            - TransYear
            - TransMonth
            - TransDay
            - TransHour
            - TransMin
            - TransSec
            - RcvYear
            - RcvMonth
            - RcvDay
            - RcvHour
            - RcvMin
            - RcvSec
            - Reserved
          properties:
            RouteID:
              type: number
              description: ????????????
            BusID:
              type: number
              description: ????????????
            CurrentStop:
              type: number
              description: ??????????????????????????????
            DestinationStop:
              type: number
              description: ???????????????????????????
            IsLastBus:
              type: number
              description: ?????????????????? 0:???????????? 1:?????????
            EstimateTime:
              type: number
              description: ??????????????????(???????????????)
            StopDistance:
              type: number
              description: ??????????????????
            Direction:
              type: number
              description: ?????? 0:?????? 1:?????? 2:???????????? 3:???????????????
            Type:
              type: number
              description: ??????????????? 1:?????? 2:?????????
              example: 1
            TransYear:
              type: number
              description: ???????????????????????? ??????,UTC ??????,?????????2000?????????
              example: 2000
            TransMonth:
              type: number
              description: 1~12
              example: 1
            TransDay:
              type: number
              description: 1~31
              example: 1
            TransHour:
              type: number
              description: 0~23
            TransMin:
              type: number
              description: 0~59
            TransSec:
              type: number
              description: 0~59
            RcvYear:
              type: number
              description: ???????????????????????? ??????,UTC ??????,?????????2000?????????
              example: 2000
            RcvMonth:
              type: number
              description: 1~12
              example: 1
            RcvDay:
              type: number
              description: 1~31
              example: 1
            RcvHour:
              type: number
              description: 0~23
            RcvMin:
              type: number
              description: 0~59
            RcvSec:
              type: number
              description: 0~59
            Reserved:
              type: number
              description: ??????
            SpectialEstimateTime:
              type: number
              description: ???????????????????????? 0:??????(???EstimateTime????????????????????? 1:???????????? 2:??????????????? 3:??????????????? 4:??????????????? 5:????????? 6:???????????? 7:???????????? 8:???????????????????????????
            MsgCContent:
              type: string
              description: ??????????????????????????????
            MsgEContent:
              type: string
              description: ?????????????????????????????????
            RouteMsgCContent:
              type: string
              description: ??????????????????????????????(???????????????)
            RouteMsgEContent:
              type: string
              description: ?????????????????????????????????(???????????????)
            VoiceAlertMode:
              type: number
              description: ?????????????????? 0:???????????? 1:???????????? (????????????[???????????? ????????????< 180???])
            Sequence:
              type: number
              description: ????????????
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)
    try:
        assert post_body, "post body should be in json."
        assert 'RouteID' in post_body, "key 'RouteID' missing"
        assert 'BusID' in post_body, "key 'BusID' missing"
        assert 'CurrentStop' in post_body, "key 'CurrentStop' missing"
        assert 'DestinationStop' in post_body, "key 'DestinationStop' missing"
        assert 'IsLastBus' in post_body, "key 'IsLastBus' missing"
        assert 'EstimateTime' in post_body, "key 'EstimateTime' missing"
        assert 'StopDistance' in post_body, "key 'StopDistance' missing"
        assert 'Direction' in post_body, "key 'Direction' missing"
        assert 'Type' in post_body, "key 'Type' missing"
        assert 'TransYear' in post_body, "key 'TransYear' missing"
        assert 'TransMonth' in post_body, "key 'TransMonth' missing"
        assert 'TransDay' in post_body, "key 'TransDay' missing"
        assert 'TransHour' in post_body, "key 'TransHour' missing"
        assert 'TransMin' in post_body, "key 'TransMin' missing"
        assert 'TransSec' in post_body, "key 'TransSec' missing"
        assert 'RcvYear' in post_body, "key 'RcvYear' missing"
        assert 'RcvMonth' in post_body, "key 'RcvMonth' missing"
        assert 'RcvDay' in post_body, "key 'RcvDay' missing"
        assert 'RcvHour' in post_body, "key 'RcvHour' missing"
        assert 'RcvMin' in post_body, "key 'RcvMin' missing"
        assert 'RcvSec' in post_body, "key 'RcvSec' missing"
        assert 'Reserved' in post_body, "key 'Reserved' missing"
        msg = create_msg(post_body, 0x07, int(stop_id))
        ack_msg = estop_auto_server.udp_server.send_update_bus_info(msg_obj=msg)
        if not ack_msg:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"TimeoutError: Did not receive ack msg.").response)
        elif ack_msg.payload.MsgStatus != 1:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"OperationError: Receive fail update report.").response)
        else:
            return jsonify(FlasggerResponse(message=f"{str(ack_msg.payload.to_dict())}").response)

    except Exception as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"{e.__class__.__name__}: {e.__str__()}").response)


@flasgger_server.route("/stopapi/v1/set_route_info/<stop_id>", methods=['POST'])
def set_route_info(stop_id):
    """ Update route info to estop.
    ---
    tags:
      - name: TTIA EStop Protocol
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

      - name: route_info
        in: body
        type: string
        required: true

        schema:
          id: route_info
          type: object
          required:
            - RouteID
            - PathCName
            - PathEName
            - Sequence
          properties:
            RouteID:
              type: number
              description: ????????????
            PathCName:
              type: string
              description: ??????????????????
            PathEName:
              type: string
              description: ??????????????????
            Sequence:
              type: number
              description: ????????????
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)
    try:
        assert post_body, "post body should be in json."
        assert 'RouteID' in post_body, "key 'RouteID' missing"
        assert 'PathCName' in post_body, "key 'PathCName' missing"
        assert 'PathEName' in post_body, "key 'PathEName' missing"
        assert 'Sequence' in post_body, "key 'Sequence' missing"
        msg = create_msg(post_body, 0x0B, int(stop_id))
        ack_msg = estop_auto_server.udp_server.send_update_route_info(msg_obj=msg)

        if not ack_msg:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"TimeoutError: Did not receive ack msg.").response)
        elif ack_msg.payload.MsgStatus != 1:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"OperationError: Receive fail update report.").response)
        else:
            return jsonify(FlasggerResponse(message=f"{str(ack_msg.payload.to_dict())}").response)
    except Exception as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"{e.__class__.__name__}: {e.__str__()}").response)


@flasgger_server.route("/stopapi/v1/set_brightness/<stop_id>", methods=['POST'])
def set_brightness(stop_id):
    """Update brightness info to estop.
    ---
    tags:
      - name: TTIA EStop Protocol
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

      - name: brightness
        in: body
        type: string
        required: true
        schema:
          id: brightness
          type: object
          required:
            - LightSet
          properties:
            LightSet:
              type: number
              description: ???????????? 0:?????? 15:??????

    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)

    try:
        assert post_body, "post body should be in json."
        assert 'LightSet' in post_body, "key 'LightSet' missing"
        msg = create_msg(post_body, 0x0D, int(stop_id))
        ack_msg = estop_auto_server.udp_server.send_set_brightness(msg_obj=msg)

        if not ack_msg:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"TimeoutError: Did not receive ack msg.").response)

        else:
            return jsonify(FlasggerResponse(message=f"{str(ack_msg.payload.to_dict())}").response)

    except Exception as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"{e.__class__.__name__}: {e.__str__()}").response)


@flasgger_server.route("/stopapi/v1/reboot/<stop_id>", methods=['POST'])
def set_reboot(stop_id):
    """reboot the stop by stop id.
    ---
    tags:
      - name: TTIA EStop Protocol
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true
    responses:
      200:
        description: Return dict message with op result.
    """
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)
    try:
        msg = create_msg({}, 0x10, int(stop_id))
        ack_msg = estop_auto_server.udp_server.send_reboot(msg_obj=msg)

        if not ack_msg:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"TimeoutError: Did not receive ack msg.").response)
        else:
            return jsonify(FlasggerResponse(message=f"{str(ack_msg.payload.to_dict())}").response)
    except Exception as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"{e.__class__.__name__}: {e.__str__()}").response)


@flasgger_server.route("/stopapi/v1/set_gif/<stop_id>", methods=['POST'])
def set_gif(stop_id):
    """Update gif info to estop.
    ---
    tags:
      - name: TTIA EStop Protocol
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

      - name: update_gif
        in: body
        type: string
        required: true
        schema:
          id: update_gif
          type: object
          required:
            - PicNo
            - PicNum
            - PicURL
            - MsgContent
          properties:
            PicNo:
              type: number
              description: ????????????
            PicNum:
              type: number
              description: ??????????????????
            PicURL:
              type: string
              description: ??????????????????
            MsgContent:
              type: string
              description: ????????????

    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)

    try:
        assert post_body, "post body should be in json."
        assert 'PicNo' in post_body, "key 'PicNo' missing"
        assert 'PicNum' in post_body, "key 'PicNum' missing"
        assert 'PicURL' in post_body, "key 'PicURL' missing"
        assert 'MsgContent' in post_body, "key 'MsgContent' missing"
        msg = create_msg(post_body, 0x12, int(stop_id))
        ack_msg = estop_auto_server.udp_server.send_update_gif(msg_obj=msg)

        if not ack_msg:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"TimeoutError: Did not receive ack msg.").response)

        else:
            return jsonify(FlasggerResponse(message=f"{str(ack_msg.payload.to_dict())}").response)
    except Exception as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"{e.__class__.__name__}: {e.__str__()}").response)


@flasgger_server.route("/stopapi/v1/update_route_info/<stop_id>", methods=['POST'])
def update_route_info(stop_id):
    """Update serious route info to estop from cache.
    ---
    tags:
      - name: TTIA EStop helper
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

    responses:
      200:
        description: Return dict message with op result.
    """
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)

    estop_auto_server.TTIAAutoStopandRouteServer.udp_server.update_route_info(stop_id=int(stop_id))

    return jsonify(FlasggerResponse().response)


@flasgger_server.route("/stopapi/v1/update_msg/<stop_id>", methods=['POST'])
def update_msg(stop_id):
    """Update msg tag to estop from cache.
    ---
    tags:
      - name: TTIA EStop helper
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

    responses:
      200:
        description: Return dict message with op result.
    """
    if not check_stop(int(stop_id))[0]:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: {check_stop(int(stop_id))[1]}").response)

    estop_auto_server.TTIAAutoMsgServer.send_msg(stop_id=int(stop_id))

    return jsonify(FlasggerResponse().response)


@flasgger_server.route("/stopapi/v1/size_monitor", methods=['POST'])
def check_caches_size():
    """Use to monitor the caches size.
    ---
    tags:
      - name: TTIA EStop helper

    responses:
      200:
        description: Return dict message with op result.
    """
    sizes = {
        "estop_cache": sys.getsizeof(EStopObjCacher.estop_cache),
        "estop_rsid_sid": sys.getsizeof(EStopObjCacher.rsid_sid_table),
        "server_udp_sections": sys.getsizeof(estop_auto_server.udp_server.sections)
    }
    return jsonify(sizes)
