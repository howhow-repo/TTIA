import logging
import socket
import threading
from datetime import datetime

logger = logging.getLogger(__name__)


class UDPWorkingSection:
    lifetime = 15  # second

    def __init__(self, stop_id, client_addr, process_id):
        self.client_addr = client_addr
        self.stop_id = stop_id
        self.start_time = datetime.now()
        self.process_id = process_id
        self.logs = [process_id]


class UDPServer:
    """ A simple UDP Server """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    section_lifetime = UDPWorkingSection.lifetime
    sections = {}
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

    @classmethod
    def expire_timeout_section(cls):
        now = datetime.now()
        should_be_del = []
        for section_id in cls.sections:
            if (now - cls.sections[section_id].start_time).seconds > UDPWorkingSection.lifetime:
                should_be_del.append(section_id)
        for section_id in should_be_del:
            del cls.sections[section_id]

    @classmethod
    def section_or_none(cls, stop_id):
        """
        :param stop_id:
        :return:
            :return section if section if found
            :return None if section not found
        """
        for section_id in cls.sections:
            if section_id == stop_id:
                return cls.sections[section_id]
        return None

    @classmethod
    def remove_from_sections(cls, stop_id):
        del cls.sections[stop_id]
