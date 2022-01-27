from .base_server import UDPServer
from lib import EStopObjCacher


class TTIAStopUdpServer(UDPServer):

    def __init__(self, host, port):
        super().__init__(host, port)

    def handle_request(self, data, client_address):
        print("data: ", data, "\n",
              "datatype: ", type(data), "\n",
              "client_address", client_address, "\n",)
        self.sock.sendto(b"echo: "+data, client_address)
