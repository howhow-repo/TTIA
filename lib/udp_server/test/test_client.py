# -*- coding: utf-8 -*-
import socket
from lib import TTIABusStopMessage


def test_reguplink():
    pdu = TTIABusStopMessage(0, 'default').to_pdu()
    HOST = 'localhost'
    PORT = 50000
    server_addr = (HOST, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(pdu, server_addr)
    indata, addr = s.recvfrom(1024)
    print('recvfrom: ', addr, "\n",
          "data: ", indata)


if __name__ == '__main__':
    test_reguplink()
