# -*- coding: utf-8 -*-
import socket
from lib import TTIABusStopMessage

STOPID = 1
HOST = 'localhost'
PORT = 50000
server_addr = (HOST, PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def test_reguplink():
    msg = TTIABusStopMessage(0, 'default')
    msg.header.StopID = STOPID
    msg.payload.IMSI = "1234567890"

    s.sendto(msg.to_pdu(), server_addr)
    indata, addr = s.recvfrom(1024)

    recv = TTIABusStopMessage(indata, 'pdu')
    print('recvfrom: ', addr, "\n",
          "data: ", recv.to_dict())

    input()
    msg = TTIABusStopMessage(2, 'default')
    msg.header.StopID = STOPID
    msg.payload.MsgStatus = 1
    s.sendto(msg.to_pdu(), server_addr)
    print("send: ", msg.to_dict())


def test_period_report():
    msg = TTIABusStopMessage(3, 'default')
    msg.header.StopID = STOPID
    msg.payload.SentCount = 33
    msg.payload.RecvCount = 66

    s.sendto(msg.to_pdu(), server_addr)
    indata, addr = s.recvfrom(1024)

    recv = TTIABusStopMessage(indata, 'pdu')
    print('recvfrom: ', addr, "\n",
          "data: ", recv.to_dict())


def test_abnormal_report():
    msg = TTIABusStopMessage(0x09, 'default')
    msg.header.StopID = STOPID
    msg.payload.StatusCode = 2

    s.sendto(msg.to_pdu(), server_addr)
    indata, addr = s.recvfrom(1024)

    recv = TTIABusStopMessage(indata, 'pdu')
    print('recvfrom: ', addr, "\n",
          "data: ", recv.to_dict())


if __name__ == '__main__':
    # test_reguplink()
    test_period_report()
