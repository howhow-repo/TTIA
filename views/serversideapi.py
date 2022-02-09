from flask import Blueprint, jsonify, request
from lib import EStopObjCacher, TTIAStopUdpServer, TTIABusStopMessage
from lib import FlasggerResponse
from decouple import config
import logging


"""
    Features in swagger page 
"""


logger = logging.getLogger(__name__)
flasgger_server = Blueprint('flasgger_server', __name__)

TTIA_UDP_PORT = config('TTIA_UDP_SERVER_PORT', cast=int, default=50000)
estop_udp_server = TTIAStopUdpServer(host="localhost", port=TTIA_UDP_PORT)


def send(post_body, message_id: int, stop_id: int):
    estop = EStopObjCacher.get_estop_by_id(stop_id)
    if estop and estop.ready and estop.address:
        try:
            msg = TTIABusStopMessage(message_id, 'default')
            msg.header.StopID = stop_id
            msg.payload.from_dict(post_body)
            msg.option_payload.from_dict(post_body)

            if message_id == 0x05:
                estop_udp_server.send_update_msg_tag(msg_obj=msg, addr=estop.address)
            elif message_id == 0x07:
                estop_udp_server.send_update_bus_info(msg_obj=msg, addr=estop.address)
            elif message_id == 0x0B:
                estop_udp_server.send_update_route_info(msg_obj=msg, addr=estop.address)
            elif message_id == 0x0D:
                estop_udp_server.send_set_brightness(msg_obj=msg, addr=estop.address)
            elif message_id == 0x10:
                estop_udp_server.send_reboot(msg_obj=msg, addr=estop.address)
            elif message_id == 0x12:
                estop_udp_server.send_update_gif(msg_obj=msg, addr=estop.address)

        except AssertionError as e:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=3,
                                            message=f"AssertionError: {e}").response)

    elif not estop:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=2,
                                        message=f"estop id {stop_id} is not found in cache.").response)
    elif not estop.ready:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=2,
                                        message=f"estop id {stop_id} is not ready yet.").response)
    elif not estop.address:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=2,
                                        message=f"can not find addr of estop id {stop_id}.").response)

    return jsonify(FlasggerResponse().response)


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


@flasgger_server.route("/stopapi/v1/get_cache/ready", methods=['GET'])
def get_cache_ready():
    """get estops those are ready registered.
    ---
    tags:
      - name: TTIA estop
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
    return jsonify(EStopObjCacher.estop_cache[int(stop_id)].to_json())


@flasgger_server.route("/stopapi/v1/reload_caches/", methods=['POST'])
def reload_caches():
    """Force cacher to reload from mysql. See more parameter description in Models below.
    ---
    tags:
      - name: TTIA estop
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
        try:
            EStopObjCacher.load_from_sql_by_estop_ids(post_body['ids'])
            logger.info(f"estop cache reloaded by id: {post_body['ids']}")
            return jsonify(FlasggerResponse(message=f"estop cache reloaded by id: [{post_body['ids']}]").response)
        except Exception as err:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=2,
                                            message=f"fail reload estop of {post_body['ids']}, {err}").response)
    else:
        try:
            EStopObjCacher.load_from_sql()
            logger.info("estop cache total reloaded")
            return jsonify(FlasggerResponse(message="estop cache total reloaded").response)
        except Exception as err:
            return jsonify(FlasggerResponse(result="fail",
                                            error_code=2,
                                            message=f"fail reload estop, {err}").response)


@flasgger_server.route("/stopapi/v1/set_msg/<stop_id>", methods=['POST'])
def set_msg(stop_id):
    """Update text msg to estop.
    ---
    tags:
      - name: TTIA estop
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
              description: 訊息標籤，控制中 心定義之訊息代碼 0:手動機制(自中心 取得所有訊息設 定，由站牌設備自行 排程) 5:自動機制(由中心 排程下送最新一筆 訊息 50:提供獨立式9字 LED站牌氣象資訊
            MsgNo:
              type: number
              description: 訊息編號
            MsgContent:
              type: string
              description: 訊息內容(big5)
            MsgPriority:
              type: number
              description: (optional) 訊息設定重要性 0:一般 1:重要 2:緊急
            MsgType:
              type: number
              description: (optional) 訊息類別 0:一般 1:分區 2:交通管制
            MsgStopDelay:
              type: number
              description: (optional) 預設:2秒 顯示訊息停等時間
              example: 2
            MsgChangeDelay:
              type: number
              description: (optional) 預設:1秒 顯示下一則訊息 翻轉停等時間
              example: 1
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    try:
        assert post_body, "post body should be in json."
        assert 'MsgTag' in post_body, "key 'MsgTag' missing"
        assert 'MsgNo' in post_body, "key 'MsgNo' missing"
        assert 'MsgContent' in post_body, "key 'MsgContent' missing"
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)

    return send(post_body, 0x05, int(stop_id))


@flasgger_server.route("/stopapi/v1/set_bus_info/<stop_id>", methods=['POST'])
def set_bus_info(stop_id):
    """Update bus info to estop.
    ---
    tags:
      - name: TTIA estop
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
              description: 路線代碼
            BusID:
              type: number
              description: 車輛代碼
            CurrentStop:
              type: number
              description: 車輛目前所在站牌代碼
            DestinationStop:
              type: number
              description: 車輛目的地站牌代碼
            IsLastBus:
              type: number
              description: 是否為末班車 0:非末班車 1:末班車
            EstimateTime:
              type: number
              description: 預估到站時間(以秒為單位)
            StopDistance:
              type: number
              description: 距離本站站數
            Direction:
              type: number
              description: 方向 0:去程 1:返程 2:尚未發車 3:末班已離駛
            Type:
              type: number
              description: 本訊息種類 1:定期 2:非定期
              example: 1
            TransYear:
              type: number
              description: 即時公車資訊傳出 時間,UTC 時間,從西元2000年起始
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
              description: 即時公車資訊傳出 時間,UTC 時間,從西元2000年起始
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
              description: 保留
            SpectialEstimateTime:
              type: number
              description: 特定預估到站資訊 0:一般(以EstimateTime為預估到站時間 1:尚未發車 2:交管不停靠 3:末班車已過 4:今日未營運 5:進站中 6:即將到站 7:發車資訊 8:特殊中英文顯示資訊
            MsgCContent:
              type: string
              description: 預估到站中文顯示內容
            MsgEContent:
              type: string
              description: 預估到站英文文顯示內容
            RouteMsgCContent:
              type: string
              description: 預估到站中文顯示內容(含路線資訊)
            RouteMsgEContent:
              type: string
              description: 預估到站英文文顯示內容(含路線資訊)
            VoiceAlertMode:
              type: number
              description: 廣播開關設定 0:功能關閉 1:功能開啟 (功能開啟[即將到站 預估時間< 180秒])
            Sequence:
              type: number
              description: 顯示順序


    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
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
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)

    return send(post_body, 0x07, int(stop_id))


@flasgger_server.route("/stopapi/v1/set_route_info/<stop_id>", methods=['POST'])
def set_route_info(stop_id):
    """Update route info to estop.
    ---
    tags:
      - name: TTIA estop
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
              description: 路線代碼
            PathCName:
              type: string
              description: 路線中文名稱
            PathEName:
              type: string
              description: 路線英文名稱
            Sequence:
              type: number
              description: 顯示順序

    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    try:
        assert post_body, "post body should be in json."
        assert 'RouteID' in post_body, "key 'RouteID' missing"
        assert 'PathCName' in post_body, "key 'PathCName' missing"
        assert 'PathEName' in post_body, "key 'PathEName' missing"
        assert 'Sequence' in post_body, "key 'Sequence' missing"
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)

    return send(post_body, 0x0B, int(stop_id))


@flasgger_server.route("/stopapi/v1/set_brightness/<stop_id>", methods=['POST'])
def set_brightness(stop_id):
    """Update route info to estop.
    ---
    tags:
      - name: TTIA estop
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
          id: route_info
          type: object
          required:
            - LightSet
          properties:
            LightSet:
              type: number
              description: 亮度設定 0:最暗 15:最亮

    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    try:
        assert post_body, "post body should be in json."
        assert 'LightSet' in post_body, "key 'LightSet' missing"
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)

    return send(post_body, 0x0D, int(stop_id))


@flasgger_server.route("/stopapi/v1/reboot/<stop_id>", methods=['POST'])
def set_reboot(stop_id):
    """reboot the stop by stop id.
    ---
    tags:
      - name: TTIA estop
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true
    responses:
      200:
        description: Return dict message with op result.
    """
    return send(request.get_json(), 0x10, int(stop_id))


@flasgger_server.route("/stopapi/v1/update_gif/<stop_id>", methods=['POST'])
def set_gif(stop_id):
    """Update gif info to estop.
    ---
    tags:
      - name: TTIA estop
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
              description: 路線代碼
            PicNum:
              type: number
              description: 路線中文名稱
            PicURL:
              type: string
              description: 路線英文名稱
            MsgContent:
              type: string
              description: 顯示順序

    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    try:
        assert post_body, "post body should be in json."
        assert 'PicNo' in post_body, "key 'PicNo' missing"
        assert 'PicNum' in post_body, "key 'PicNum' missing"
        assert 'PicURL' in post_body, "key 'PicURL' missing"
        assert 'MsgContent' in post_body, "key 'MsgContent' missing"
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)
    return send(post_body, 0x12, int(stop_id))
