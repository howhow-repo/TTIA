import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from decouple import config
from .serversideapi import estop_udp_server
from lib import EStopObjCacher, TTIAStopUdpServer, TTIABusStopMessage
from lib import FlasggerResponse


logger = logging.getLogger(__name__)
scheduler_api = Blueprint('scheduler_api', __name__)

TIMEZONE = config('TIMEZONE', default="Asia/Taipei")
scheduler = BackgroundScheduler(timezone=TIMEZONE)
scheduler.add_job(func=EStopObjCacher.load_from_sql,
                  trigger=CronTrigger(
                      hour="00",
                      minute="01",
                      timezone=TIMEZONE
                  ),
                  id='cache_daily_reload',
                  max_instances=1,
                  replace_existing=True, )

scheduler.add_job(func=TTIAStopUdpServer.expire_timeout_section,
                  trigger='interval',
                  id='expire_timeout_section',
                  seconds=TTIAStopUdpServer.section_lifetime / 2)


@scheduler_api.route("/stopapi/v1/get_jobs/", methods=['GET'])
def get_jobs():
    """get jobs from background scheduler.
    ---
    tags:
      - name: scheduler
    responses:
      200:
        description: Return the current cache of estop id
    """
    return jsonify(
        [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in scheduler.get_jobs()]
    )


@scheduler_api.route("/stopapi/v1/add_msg_update_schedule/<stop_id>", methods=['POST'])
def add_update_msg(stop_id):
    """add update msg mission to server.
    ---
    tags:
      - name: scheduler
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
            - UpdateTime
            - MsgTag
            - MsgNo
            - MsgContent
          properties:
            UpdateTime:
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
        assert 'UpdateTime' in post_body, "key 'UpdateTime' missing"
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
        update_time = datetime.strptime(post_body['UpdateTime'], dateFormatter)
    except ValueError as e:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"ValueError: {e}").response)

    msg = TTIABusStopMessage(0x05, 'default')
    msg.header.StopID = int(stop_id)
    msg.payload.from_dict(post_body)
    msg.option_payload.from_dict(post_body)
    estop = EStopObjCacher.get_estop_by_id(stop_id)

    if estop and estop.ready and estop.address:
        scheduler.add_job(func=lambda: estop_udp_server.send_update_msg_tag(msg, estop.address),
                          next_run_time=update_time,
                          max_instances=1,)
    else:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: The estop is not found or not ready yet.").response)

    return jsonify(
        [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in scheduler.get_jobs()]
    )
