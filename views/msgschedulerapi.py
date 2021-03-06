import logging
from datetime import datetime
from flask import Blueprint, jsonify, request
from .serversideapi import estop_auto_server
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
            estop_auto_server.TTIAAutoMsgServer.scheduler.add_job(func=lambda: send_update_msg_tag(msg),
                                  next_run_time=trigger_time,
                                  max_instances=1, )
        elif message_id == 0x07:
            estop_auto_server.TTIAAutoMsgServer.scheduler.add_job(func=lambda: send_update_bus_info(msg),
                                  next_run_time=trigger_time,
                                  max_instances=1, )
        elif message_id == 0x0B:
            estop_auto_server.TTIAAutoMsgServer.scheduler.add_job(func=lambda: send_update_route_info(msg),
                                  next_run_time=trigger_time,
                                  max_instances=1, )
        elif message_id == 0x12:
            estop_auto_server.TTIAAutoMsgServer.scheduler.add_job(func=lambda: send_update_gif(msg),
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
         estop_auto_server.TTIAAutoMsgServer.scheduler.get_jobs()]
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
         estop_auto_server.TTIAAutoMsgServer.scheduler.get_jobs()]
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

    if estop_auto_server.TTIAAutoMsgServer.scheduler.get_job(post_body['job_id']):
        estop_auto_server.TTIAAutoMsgServer.scheduler.remove_job(post_body['job_id'])
    else:
        return jsonify(FlasggerResponse(result="fail",
                                        error_code=3,
                                        message=f"StatusError: did not find job id.").response)

    return jsonify(
        [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in
         estop_auto_server.TTIAAutoMsgServer.scheduler.get_jobs()]
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
        estop_auto_server.TTIAAutoMsgServer.reload_msg()
        return jsonify(
            [f"id: {job.id}, name: {job.name}, trigger: {job.trigger}, next: {job.next_run_time}" for job in
             estop_auto_server.TTIAAutoMsgServer.scheduler.get_jobs()]
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
