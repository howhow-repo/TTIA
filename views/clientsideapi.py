from flask import Blueprint, jsonify, request
from lib import TTIAEStopUdpClient, TTIABusStopMessage
from lib import EStop
from decouple import config

"""
    Features in swagger page 
"""

flasgger_client = Blueprint('flasgger_client', __name__)

TTIA_UDP_PORT = config('TTIA_UDP_CLIENT_PORT', cast=int, default=50000)
estop = EStop({"StopID": 5, "IMSI": '509894234641555'})
estop_udp_server = TTIAEStopUdpClient(host="localhost", port=TTIA_UDP_PORT, estop=estop,
                                      server_host='localhost', server_port=50000)


class OperationResponse:
    def __init__(self, result: str = 'success', error_code: int = 0, message: str = None):
        r = {
            'result': result,
            'error_code': error_code,
        }
        if message is not None:
            r['message'] = message
        self.response = r


@flasgger_client.route("/clientapi/v1/info", methods=['GET'])
def get_self_info():
    """get self estop client current info.
    ---
    tags:
      - name: TTIA estop client
    responses:
      200:
        description: Return the current syayus of estops
    """
    print(estop.to_json())
    try:
        return jsonify(estop.to_json())
    except Exception as err:
        return jsonify(OperationResponse(result="fail",
                                         error_code=2,
                                         message=f"fail get estop info, {err}").response)


@flasgger_client.route("/clientapi/v1/send_registration/", methods=['POST'])
def registrate_estop():
    """Send registration to server side.
    ---
    tags:
      - name: TTIA estop client
    responses:
      200:
        description: Return dict message with op result.
    """
    try:
        estop_udp_server.send_registration()
    except Exception as err:
        return jsonify(OperationResponse(result="fail",
                                         error_code=2,
                                         message=f"fail reload estop, {err}").response)

    return jsonify(OperationResponse().response)


@flasgger_client.route("/clientapi/v1/send_period_report/", methods=['POST'])
def period_report():
    """Send period report to server side.
    ---
    tags:
      - name: TTIA estop client
    responses:
      200:
        description: Return dict message with op result.
    """
    try:
        estop_udp_server.send_period_report()
    except Exception as err:
        return jsonify(OperationResponse(result="fail",
                                         error_code=2,
                                         message=f"fail reload estop, {err}").response)

    return jsonify(OperationResponse().response)


@flasgger_client.route("/clientapi/v1/abnormal/", methods=['POST'])
def abnormal_report():
    """Send abnormal report to server via udp.
    ---
    tags:
      - name: TTIA estop client
    parameters:
      - name: report info
        in: body
        type: string
        required: true
        schema:
          id: abnormal
          type: object
          required:
            - StatusCode
            - Type
          properties:
            StatusCode:
              type: number
              description: 站牌錯誤代碼 0:正常 1:站牌斷線 2:字幕機斷線
            Type:
              type: number
              description: 訊息種類 1:定期 2:非定期
    responses:
      200:
        description: Return dict message with op result.
    """

    post_body = request.get_json()

    try:
        assert post_body, "post body should be in json."
        assert 'StatusCode' in post_body, "key 'StatusCode' missing"
        assert 'Type' in post_body, "key 'Type' missing"
    except AssertionError as e:
        return jsonify(OperationResponse(result="fail",
                                         error_code=3,
                                         message=f"AssertionError: {e}").response)

    msg = TTIABusStopMessage(0x09, 'default')
    msg.payload.StatusCode = post_body['StatusCode']
    msg.payload.Type = post_body['Type']

    try:
        estop_udp_server.send_abnormal(msg)
        estop_udp_server.estop.abnormal_log.append(msg.payload.to_dict())

    except Exception as err:
        return jsonify(OperationResponse(result="fail",
                                         error_code=2,
                                         message=f"fail reload estop, {err}").response)

    return jsonify(OperationResponse().response)
