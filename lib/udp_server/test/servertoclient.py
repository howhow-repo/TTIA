# -*- coding: utf-8 -*-
import unittest
import requests


class TestServerSendMessages(unittest.TestCase):
    """Please make sure to turn on server and client is ready & registered before run testing."""
    server_ip = "localhost"
    server_port = 5000
    test_client_id = 492

    def test_send_reboot(self):
        r = requests.post(
            f'http://{self.server_ip}:{self.server_port}/stopapi/v1/reboot/{self.test_client_id}',
        )
        self.assertEqual(r.json()['result'], 'success')
        self.assertEqual(r.json()['error_code'], 0)

    def test_set_brightness(self):
        body = {"LightSet": 15}
        r = requests.post(
            f'http://{self.server_ip}:{self.server_port}/stopapi/v1/set_brightness/{self.test_client_id}', json=body
        )
        self.assertEqual(r.json()['result'], 'success')
        self.assertEqual(r.json()['error_code'], 0)

    def test_set_bus_info(self):
        body = {
            "BusID": 0,
            "CurrentStop": 0,
            "DestinationStop": 0,
            "Direction": 0,
            "EstimateTime": 0,
            "IsLastBus": 0,
            "MsgCContent": "string",
            "MsgEContent": "string",
            "RcvDay": 1,
            "RcvHour": 0,
            "RcvMin": 0,
            "RcvMonth": 1,
            "RcvSec": 0,
            "RcvYear": 2000,
            "Reserved": 0,
            "RouteID": 0,
            "RouteMsgCContent": "string",
            "RouteMsgEContent": "string",
            "Sequence": 0,
            "SpectialEstimateTime": 0,
            "StopDistance": 0,
            "TransDay": 1,
            "TransHour": 0,
            "TransMin": 0,
            "TransMonth": 1,
            "TransSec": 0,
            "TransYear": 2000,
            "Type": 1,
            "VoiceAlertMode": 0
        }
        r = requests.post(
            f'http://{self.server_ip}:{self.server_port}/stopapi/v1/set_bus_info/{self.test_client_id}', json=body
        )
        self.assertEqual(r.json()['result'], 'success')
        self.assertEqual(r.json()['error_code'], 0)

    def test_set_msg(self):
        body = {
            "MsgChangeDelay": 1,
            "MsgContent": "string",
            "MsgNo": 0,
            "MsgPriority": 0,
            "MsgStopDelay": 2,
            "MsgTag": 0,
            "MsgType": 0
        }
        r = requests.post(
            f'http://{self.server_ip}:{self.server_port}/stopapi/v1/set_msg/{self.test_client_id}', json=body
        )
        self.assertEqual(r.json()['result'], 'success')
        self.assertEqual(r.json()['error_code'], 0)

    def test_set_route_info(self):
        body = {
            "PathCName": "中文站名長",
            "PathEName": "string",
            "RouteID": 6553,
            "Sequence": 0
        }
        r = requests.post(
            f'http://{self.server_ip}:{self.server_port}/stopapi/v1/set_route_info/{self.test_client_id}', json=body
        )
        self.assertEqual(r.json()['result'], 'success')
        self.assertEqual(r.json()['error_code'], 0)

    def test_update_gif(self):
        body = {
            "MsgContent": "string",
            "PicNo": 0,
            "PicNum": 0,
            "PicURL": "string"
        }
        r = requests.post(
            f'http://{self.server_ip}:{self.server_port}/stopapi/v1/set_gif/{self.test_client_id}', json=body
        )
        self.assertEqual(r.json()['result'], 'success')
        self.assertEqual(r.json()['error_code'], 0)
