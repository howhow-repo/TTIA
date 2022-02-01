from .base_server import UDPServer
from lib import TTIABusStopMessage
import logging

logger = logging.getLogger(__name__)


def decode_msg(data):
    try:
        return TTIABusStopMessage(data, 'pdu')
    except AssertionError:
        return False


class ClientSideHandler(UDPServer):
    def __init__(self, host, port):
        super().__init__(host, port)

    def handle_request(self, data, client_address):
        msg_obj = decode_msg(data)
        if not msg_obj:  # quick fail if data not ttia format
            return

        if msg_obj.header.MessageID in [0x00, 0x03, 0x09]:
            pass  # should send by client, ignore.
        elif msg_obj.header.MessageID in [0x02, 0x06, 0x0C, 0x0E, 0x13]:
            pass  # should response from client, ignore

        elif msg_obj.header.MessageID == 0x01:
            self.recv_registration_info(msg_obj)
        elif msg_obj.header.MessageID == 0x04:
            self.recv_period_report_check(msg_obj)
        elif msg_obj.header.MessageID == 0x05:
            self.recv_update_msg_tag(msg_obj)
        elif msg_obj.header.MessageID == 0x07:
            self.recv_update_bus_info(msg_obj)
        elif msg_obj.header.MessageID == 0x0A:
            self.recv_abnormal_check(msg_obj)
        elif msg_obj.header.MessageID == 0x0B:
            self.recv_update_route_info(msg_obj)
        elif msg_obj.header.MessageID == 0x0D:
            self.recv_set_brightness(msg_obj)
        elif msg_obj.header.MessageID == 0x10:
            self.recv_reboot(msg_obj)
        elif msg_obj.header.MessageID == 0x12:
            self.recv_update_gif(msg_obj)

        else:
            print("drop msg with unknown message id.")

    #### TTIA estop behaviors
    def send_registration(self):  # 0x00
        raise NotImplementedError

    def recv_registration_info(self, msg_obj: TTIABusStopMessage):  # 0x01
        raise NotImplementedError

    def send_registration_info_check(self, msg_obj: TTIABusStopMessage):  # 0x02
        raise NotImplementedError

    def send_period_report(self):  # 0x03
        raise NotImplementedError

    def recv_period_report_check(self, msg_obj: TTIABusStopMessage):  # 0x04
        raise NotImplementedError

    def recv_update_msg_tag(self, msg_obj: TTIABusStopMessage):  # 0x05
        raise NotImplementedError

    def send_update_msg_tag_check(self, msg_obj: TTIABusStopMessage):  # 0x06
        raise NotImplementedError

    def recv_update_bus_info(self, msg_obj: TTIABusStopMessage):  # 0x07
        raise NotImplementedError

    def send_update_bus_info_check(self, msg_obj: TTIABusStopMessage):  # 0x08
        raise NotImplementedError

    def send_abnormal(self, msg_obj: TTIABusStopMessage):  # 0x09
        raise NotImplementedError

    def recv_abnormal_check(self, msg_obj: TTIABusStopMessage):  # 0x0A
        raise NotImplementedError

    def recv_update_route_info(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def send_update_route_info_check(self, msg_obj: TTIABusStopMessage):  # 0x0C
        raise NotImplementedError

    def recv_set_brightness(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def send_set_brightness_check(self, msg_obj: TTIABusStopMessage):  # 0x0C
        raise NotImplementedError

    def recv_reboot(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def send_reboot_check(self, msg_obj: TTIABusStopMessage):  # 0x0C
        raise NotImplementedError

    def recv_update_gif(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def send_update_gif_check(self, msg_obj: TTIABusStopMessage):  # 0x0C
        raise NotImplementedError
