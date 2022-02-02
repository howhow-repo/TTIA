from flask import Blueprint, jsonify, request
from lib import EStopObjCacher, TTIAStopUdpServer, TTIABusStopMessage
from decouple import config

"""
    Features in swagger page 
"""

flasgger_server = Blueprint('flasgger_server', __name__)

TTIA_UDP_PORT = config('TTIA_UDP_SERVER_PORT', cast=int, default=50000)
estop_udp_server = TTIAStopUdpServer(host="localhost", port=TTIA_UDP_PORT)


class OperationResponse:
    def __init__(self, result: str = 'success', error_code: int = 0, message: str = None):
        r = {
            'result': result,
            'error_code': error_code,
        }
        if message is not None:
            r['message'] = message
        self.response = r


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
    if len(post_body['ids']) == 0:
        try:
            EStopObjCacher.load_from_sql()
        except Exception as err:
            return jsonify(OperationResponse(result="fail",
                                             error_code=2,
                                             message=f"fail reload estop, {err}").response)
    elif len(post_body['ids']) > 0:
        try:
            EStopObjCacher.load_from_sql_by_estop_ids(post_body['ids'])
        except Exception as err:
            return jsonify(OperationResponse(result="fail",
                                             error_code=2,
                                             message=f"fail reload estop of {post_body['ids']}, {err}").response)

    return jsonify(OperationResponse().response)


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
    stop_id = int(stop_id)
    estop = EStopObjCacher.get_estop_by_id(stop_id)
    if estop and estop.ready and estop.address:
        section = estop_udp_server.create_new_section(stop_id, estop.address, 0x05)
        msg = TTIABusStopMessage(0x05, 'default')
        msg.header.StopID = stop_id
        msg.payload.from_dict(post_body)
        msg.option_payload.from_dict(post_body)
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
          type: string
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
    stop_id = int(stop_id)
    estop = EStopObjCacher.get_estop_by_id(stop_id)
    if estop and estop.ready and estop.address:
        section = estop_udp_server.create_new_section(stop_id, estop.address, 0x07)
        msg = TTIABusStopMessage(0x07, 'default')
        msg.header.StopID = stop_id
        msg.payload.from_dict(post_body)
        msg.option_payload.from_dict(post_body)
        estop_udp_server.send_update_bus_info(msg_obj=msg, section=section)

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