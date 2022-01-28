import logging
import socket
import threading
from datetime import datetime

logger = logging.getLogger(__name__)


class UDPServer:
    """ A simple UDP Server """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    EchoMode = False

    def __init__(self, host, port):
        self.host = host  # Host address
        self.port = port  # Host port

    def start(self, EchoMode=False):
        self.EchoMode = EchoMode
        logger.info("Staring estop udp server...")
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        try:
            logger.info(f"Estop udp server started at {self.host}:{self.port}")
            while True:  # keep alive
                try:  # receive request from client
                    data, client_address = self.sock.recvfrom(1024)
                    threading.Thread(target=self.handle_request, args=(data, client_address)).start()
                except OSError as err:
                    logger.error(f"UDP server error.\n {err}")
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.sock.close()
        logger.info(f"UDP server shut down.")

    def handle_request(self, data, client_address):
        if self.EchoMode:
            self.sock.sendto(b"echo: " + data, client_address)
        else:
            raise NotImplementedError
