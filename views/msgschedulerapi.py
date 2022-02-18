import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from .serversideapi import estop_auto_server, msg_scheduler
from lib import EStopObjCacher, TTIABusStopMessage
from lib import FlasggerResponse

logger = logging.getLogger(__name__)
scheduler_api = Blueprint('scheduler_api', __name__)


def send_update_msg_tag(msg):
    try:
        estop_auto_server.send_update_msg_tag(msg)
    except AssertionError as e:
        logger.error(f"{e}, fail to send_update_msg_tag")


def send_update_bus_info(msg):
    try:
        estop_auto_server.send_update_bus_info(msg)
    except AssertionError as e:
        logger.error(f"{e}, fail to send_update_bus_info")


def send_update_route_info(msg):
    try:
        estop_auto_server.send_update_route_info(msg)
    except AssertionError as e:
        logger.error(f"{e}, fail to send_update_route_info")


def send_update_gif(msg):
    try:
        estop_auto_server.send_update_gif(msg)
    except AssertionError as e:
        logger.error(f"{e}, fail to send_update_gif")


def add_launch_job(post_body, message_id: int, stop_id: int, trigger_time: datetime):
    msg = TTIABusStopMessage(message_id, 'default')
    msg.header.StopID = int(stop_id)
    msg.payload.from_dict(post_body)
    msg.option_payload.from_dict(post_body)
    estop = EStopObjCacher.get_estop_by_id(stop_id)

    if estop and estop.ready:
        if message_id == 0x05:
            msg_scheduler.add_job(func=lambda: send_update_msg_tag(msg),
                                  next_run_time=trigger_time,
                                  max_instances=1, )
        elif message_id == 0x07:
            msg_scheduler.add_job(func=lambda: send_update_bus_info(msg),
                                  next_run_time=trigger_time,
                                  max_instances=1, )
        elif message_id == 0x0B:
            msg_scheduler.add_job(func=lambda: send_update_route_info(msg),
                                  next_run_time=trigger_time,
                                  max_instances=1, )
        elif message_id == 0x12:
            msg_scheduler.add_job(func=lambda: send_update_gif(msg),
                                  next_run_time=trigger_time,
                                  max_instances=1, )
        else:
            raise NotImplementedError("Message id not implement yet.")
    else:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: The estop is not found or not ready yet.").response)

    return jsonify(
        [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in
         msg_scheduler.get_jobs()]
    )


@scheduler_api.route("/stopapi/v1/get_jobs/", methods=['GET'])
def get_jobs():
    """get jobs from background scheduler.
    ---
    tags:
      - name: msg scheduler
    responses:
      200:
        description: Return the current cache of estop id
    """
    return jsonify(
        [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in
         msg_scheduler.get_jobs()]
    )


@scheduler_api.route("/stopapi/v1/del_schedule/", methods=['DELETE'])
def del_job():
    """remove current waiting job by id.
    ---
    tags:
      - name: msg scheduler
    parameters:
      - name: del_job
        in: body
        type: string
        required: true

        schema:
          id: del_job
          type: object
          required:
            - job_id
          properties:
            job_id:
              type: string
              description: job id that you want to remove
    responses:
      200:
        description: Return dict message with op result.
    """
    post_body = request.get_json()
    try:
        assert post_body, "post body should be in json."
        assert 'job_id' in post_body, "key 'job_id' missing"
        assert post_body['job_id'] != "expire_timeout_section", "you can not remove server's period job."
        assert post_body['job_id'] != "cache_daily_reload", "you can not remove server's period job."
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    if msg_scheduler.get_job(post_body['job_id']):
        msg_scheduler.remove_job(post_body['job_id'])
    else:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: did not find job id.").response)

    return jsonify(
        [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in
         msg_scheduler.get_jobs()]
    )


@scheduler_api.route("/stopapi/v1/msg_update_schedule/reload", methods=['POST'])
def reload_msg_from_sql():
    """reload waiting update msg from sql, and automatically add into scheduler.
    ---
    tags:
      - name: msg scheduler
    responses:
      200:
        description: Return dict message with op result.
    """

    try:
        estop_auto_server.reload_msg()
        return jsonify(
            [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in
             msg_scheduler.get_jobs()]
        )
    except Exception as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"{e.__class__.__name__}: {e}").response)


@scheduler_api.route("/stopapi/v1/msg_update_schedule/<stop_id>", methods=['POST'])
def add_update_msg(stop_id):
    """add update msg mission to server.
    ---
    tags:
      - name: msg scheduler
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

      - name: msg_update_schedule
        in: body
        type: string
        required: true

        schema:
          id: msg_update_schedule
          type: object
          required:
            - LaunchTime
            - MsgTag
            - MsgNo
            - MsgContent
          properties:
            LaunchTime:
              type: string
              description: "%Y/%m/%d, %H:%M:%S"
              example: 2022/2/08, 15:00:00
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
    dateFormatter = "%Y/%m/%d, %H:%M:%S"
    try:
        stop_id = int(stop_id)
        assert post_body, "post body should be in json."
        assert 'LaunchTime' in post_body, "key 'LaunchTime' missing"
        assert 'MsgTag' in post_body, "key 'MsgTag' missing"
        assert 'MsgNo' in post_body, "key 'MsgNo' missing"
        assert 'MsgContent' in post_body, "key 'MsgContent' missing"
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    try:
        update_time = datetime.strptime(post_body['LaunchTime'], dateFormatter)
        del post_body['LaunchTime']
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    return add_launch_job(post_body, 0x05, stop_id, update_time)


@scheduler_api.route("/stopapi/v1/route_info_update_schedule/<stop_id>", methods=['POST'])
def add_update_route_info(stop_id):
    """add update route info mission to server.
    ---
    tags:
      - name: route_info scheduler
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

      - name: route_update_schedule
        in: body
        type: string
        required: true

        schema:
          id: route_update_schedule
          type: object
          required:
            - LaunchTime
            - RouteID
            - PathCName
            - PathEName
            - Sequence
          properties:
            LaunchTime:
              type: string
              description: "%Y/%m/%d, %H:%M:%S"
              example: 2022/2/08, 15:00:00
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
    dateFormatter = "%Y/%m/%d, %H:%M:%S"
    try:
        stop_id = int(stop_id)
        assert post_body, "post body should be in json."
        assert 'LaunchTime' in post_body, "key 'LaunchTime' missing"
        assert 'RouteID' in post_body, "key 'RouteID' missing"
        assert 'PathCName' in post_body, "key 'PathCName' missing"
        assert 'PathEName' in post_body, "key 'PathEName' missing"
        assert 'Sequence' in post_body, "key 'Sequence' missing"
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    try:
        update_time = datetime.strptime(post_body['LaunchTime'], dateFormatter)
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    return add_launch_job(post_body, 0x0B, stop_id, update_time)


@scheduler_api.route("/stopapi/v1/gif_update_schedule/<stop_id>", methods=['POST'])
def add_update_gif(stop_id):
    """add update gif mission to server.
    ---
    tags:
      - name: update gif scheduler
    parameters:
      - name: stop_id
        in: path
        type: number
        required: true

      - name: route_update_gif
        in: body
        type: string
        required: true

        schema:
          id: route_update_gif
          type: object
          required:
            - LaunchTime
            - PicNo
            - PicNum
            - PicURL
            - MsgContent
          properties:
            LaunchTime:
              type: string
              description: "%Y/%m/%d, %H:%M:%S"
              example: 2022/2/08, 15:00:00
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
    dateFormatter = "%Y/%m/%d, %H:%M:%S"
    try:
        stop_id = int(stop_id)
        assert post_body, "post body should be in json."
        assert 'LaunchTime' in post_body, "key 'LaunchTime' missing"
        assert 'PicNo' in post_body, "key 'PicNo' missing"
        assert 'PicNum' in post_body, "key 'PicNum' missing"
        assert 'PicURL' in post_body, "key 'PicURL' missing"
        assert 'MsgContent' in post_body, "key 'MsgContent' missing"
    except AssertionError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"AssertionError: {e}").response)
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    try:
        update_time = datetime.strptime(post_body['LaunchTime'], dateFormatter)
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    return add_launch_job(post_body, 0x012, stop_id, update_time)


# @scheduler_api.route("/stopapi/v1/bus_info_update_schedule/<stop_id>", methods=['POST'])
# def add_update_bus_info(stop_id):
#     """add update bus info mission to server.
#     ---
#     tags:
#       - name: bus_info scheduler
#     parameters:
#       - name: stop_id
#         in: path
#         type: number
#         required: true
#
#       - name: bus_info_update_schedule
#         in: body
#         type: string
#         required: true
#
#         schema:
#           id: bus_info_update_schedule
#           type: object
#           required:
#             - LaunchTime
#             - RouteID
#             - BusID
#             - CurrentStop
#             - DestinationStop
#             - IsLastBus
#             - EstimateTime
#             - StopDistance
#             - Direction
#             - Type
#             - TransYear
#             - TransMonth
#             - TransDay
#             - TransHour
#             - TransMin
#             - TransSec
#             - RcvYear
#             - RcvMonth
#             - RcvDay
#             - RcvHour
#             - RcvMin
#             - RcvSec
#             - Reserved
#           properties:
#             LaunchTime:
#               type: string
#               description: "%Y/%m/%d, %H:%M:%S"
#               example: 2022/2/08, 15:00:00
#             RouteID:
#               type: number
#               description: 路線代碼
#             BusID:
#               type: number
#               description: 車輛代碼
#             CurrentStop:
#               type: number
#               description: 車輛目前所在站牌代碼
#             DestinationStop:
#               type: number
#               description: 車輛目的地站牌代碼
#             IsLastBus:
#               type: number
#               description: 是否為末班車 0:非末班車 1:末班車
#             EstimateTime:
#               type: number
#               description: 預估到站時間(以秒為單位)
#             StopDistance:
#               type: number
#               description: 距離本站站數
#             Direction:
#               type: number
#               description: 方向 0:去程 1:返程 2:尚未發車 3:末班已離駛
#             Type:
#               type: number
#               description: 本訊息種類 1:定期 2:非定期
#               example: 1
#             TransYear:
#               type: number
#               description: 即時公車資訊傳出 時間,UTC 時間,從西元2000年起始
#               example: 2000
#             TransMonth:
#               type: number
#               description: 1~12
#               example: 1
#             TransDay:
#               type: number
#               description: 1~31
#               example: 1
#             TransHour:
#               type: number
#               description: 0~23
#             TransMin:
#               type: number
#               description: 0~59
#             TransSec:
#               type: number
#               description: 0~59
#             RcvYear:
#               type: number
#               description: 即時公車資訊傳出 時間,UTC 時間,從西元2000年起始
#               example: 2000
#             RcvMonth:
#               type: number
#               description: 1~12
#               example: 1
#             RcvDay:
#               type: number
#               description: 1~31
#               example: 1
#             RcvHour:
#               type: number
#               description: 0~23
#             RcvMin:
#               type: number
#               description: 0~59
#             RcvSec:
#               type: number
#               description: 0~59
#             Reserved:
#               type: number
#               description: 保留
#             SpectialEstimateTime:
#               type: number
#               description: 特定預估到站資訊 0:一般(以EstimateTime為預估到站時間 1:尚未發車 2:交管不停靠 3:末班車已過 4:今日未營運 5:進站中 6:即將到站 7:發車資訊 8:特殊中英文顯示資訊
#             MsgCContent:
#               type: string
#               description: 預估到站中文顯示內容
#             MsgEContent:
#               type: string
#               description: 預估到站英文文顯示內容
#             RouteMsgCContent:
#               type: string
#               description: 預估到站中文顯示內容(含路線資訊)
#             RouteMsgEContent:
#               type: string
#               description: 預估到站英文文顯示內容(含路線資訊)
#             VoiceAlertMode:
#               type: number
#               description: 廣播開關設定 0:功能關閉 1:功能開啟 (功能開啟[即將到站 預估時間< 180秒])
#             Sequence:
#               type: number
#               description: 顯示順序
#     responses:
#       200:
#         description: Return dict message with op result.
#     """
#     post_body = request.get_json()
#     dateFormatter = "%Y/%m/%d, %H:%M:%S"
#     try:
#         stop_id = int(stop_id)
#         assert post_body, "post body should be in json."
#         assert 'LaunchTime' in post_body, "key 'LaunchTime' missing"
#         assert 'RouteID' in post_body, "key 'RouteID' missing"
#         assert 'BusID' in post_body, "key 'BusID' missing"
#         assert 'CurrentStop' in post_body, "key 'CurrentStop' missing"
#         assert 'DestinationStop' in post_body, "key 'DestinationStop' missing"
#         assert 'IsLastBus' in post_body, "key 'IsLastBus' missing"
#         assert 'EstimateTime' in post_body, "key 'EstimateTime' missing"
#         assert 'StopDistance' in post_body, "key 'StopDistance' missing"
#         assert 'Direction' in post_body, "key 'Direction' missing"
#         assert 'Type' in post_body, "key 'Type' missing"
#         assert 'TransYear' in post_body, "key 'TransYear' missing"
#         assert 'TransMonth' in post_body, "key 'TransMonth' missing"
#         assert 'TransDay' in post_body, "key 'TransDay' missing"
#         assert 'TransHour' in post_body, "key 'TransHour' missing"
#         assert 'TransMin' in post_body, "key 'TransMin' missing"
#         assert 'TransSec' in post_body, "key 'TransSec' missing"
#         assert 'RcvYear' in post_body, "key 'RcvYear' missing"
#         assert 'RcvMonth' in post_body, "key 'RcvMonth' missing"
#         assert 'RcvDay' in post_body, "key 'RcvDay' missing"
#         assert 'RcvHour' in post_body, "key 'RcvHour' missing"
#         assert 'RcvMin' in post_body, "key 'RcvMin' missing"
#         assert 'RcvSec' in post_body, "key 'RcvSec' missing"
#         assert 'Reserved' in post_body, "key 'Reserved' missing"
#     except AssertionError as e:
#         return jsonify(FlasggerResponse(result="fail",
#                                         error_code=3,
#                                         message=f"AssertionError: {e}").response)
#     except ValueError as e:
#         return jsonify(FlasggerResponse(result="fail",
#                                         error_code=3,
#                                         message=f"ValueError: {e}").response)
#
#     try:
#         update_time = datetime.strptime(post_body['LaunchTime'], dateFormatter)
#     except ValueError as e:
#         return jsonify(FlasggerResponse(result="fail",
#                                         error_code=3,
#                                         message=f"ValueError: {e}").response)
#
#     return add_launch_job(post_body, 0x07, stop_id, update_time)
