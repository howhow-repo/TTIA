import datetime
import logging
from datetime import datetime
from .core import ClientSideHandler
from ..TTIA_stop_message import TTIABusStopMessage
from ..estop import EStop


logger = logging.getLogger(__name__)


class TTIAEStopUdpClient(ClientSideHandler):
    def __init__(self, host, port, estop: EStop, server_host, server_port):
        super().__init__(host, port)
        self.estop = estop
        self.server_addr = (server_host, server_port)

    def create_defaule_msg(self, msg_id: int):
        msg = TTIABusStopMessage(msg_id, 'default')
        msg.header.StopID = self.estop.StopID
        return msg

    def send_registration(self):
        logger.info('send_registration')
        msg = self.create_defaule_msg(0)
        msg.payload.IMSI = self.estop.IMSI
        msg.payload.IMEI = self.estop.IMEI
        self.sock.sendto(msg.to_pdu(), self.server_addr)

    def recv_registration_info(self, msg_obj: TTIABusStopMessage):
        logger.info(f"recv_registration_info: {msg_obj.payload.to_dict()} \n {msg_obj.option_payload.to_dict()}")
        resp_msg = self.create_defaule_msg(2)
        if msg_obj.payload.Result == 1:
            self.estop.from_dict(msg_obj.payload.to_dict())
            resp_msg.payload.MsgStatus = 1
        self.send_registration_info_ack(resp_msg)

    def send_registration_info_ack(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x02
        logger.info("send registration_info_ack")
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)

    def send_period_report(self):
        logger.info("send_period_report")
        msg = self.create_defaule_msg(0x03)
        self.estop.SentCount += 1
        msg.payload.SentCount = self.estop.SentCount
        msg.payload.RevCount = self.estop.RevCount
        self.sock.sendto(msg.to_pdu(), self.server_addr)

    def recv_period_report_ack(self, msg_obj: TTIABusStopMessage):
        logger.info("recv_period_report_ack")
        self.estop.RevCount += 1

    def recv_update_msg_tag(self, msg_obj: TTIABusStopMessage):
        logger.info(f"recv_update_msg_tag: {msg_obj.payload.to_dict()} \n {msg_obj.option_payload.to_dict()}")
        resp_msg = self.create_defaule_msg(0x06)
        resp_msg.payload.MsgTag = msg_obj.payload.MsgTag
        resp_msg.payload.MsgNo = msg_obj.payload.MsgNo
        resp_msg.payload.MsgStatus = 1
        self.send_update_msg_tag_ack(resp_msg)

    def send_update_msg_tag_ack(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x06
        logger.info('send_update_msg_tag_ack')
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)

    def recv_update_bus_info(self, msg_obj: TTIABusStopMessage):
        logger.info(f"recv_update_bus_info: {msg_obj.payload.to_dict()} \n {msg_obj.option_payload.to_dict()}")
        resp_msg = self.create_defaule_msg(0x08)
        resp_msg.payload.MsgStatus = 1
        self.estop.ready = True
        self.send_update_bus_info_ack(resp_msg)

    def send_update_bus_info_ack(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x08
        logger.info('send_update_bus_info_ack')
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)

    def send_abnormal(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x09
        logger.info(f'send_abnormal: {msg_obj.payload.to_dict()}')
        msg_obj.header.StopID = self.estop.StopID
        self.estop.abnormal_log.append(msg_obj.payload)
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)

    def recv_abnormal_ack(self, msg_obj: TTIABusStopMessage):
        self.estop.abnormal_log[-1].set_Rcv_time(datetime.now())
        logger.info(f'recv_abnormal_ack: {msg_obj.payload.to_dict()}')

    def recv_update_route_info(self, msg_obj: TTIABusStopMessage):
        logger.info(f"recv_update_route_info: {msg_obj.payload.to_dict()} \n {msg_obj.option_payload.to_dict()}")
        resp_msg = self.create_defaule_msg(0x0C)
        resp_msg.payload.MsgStatus = 1
        self.send_update_route_info_ack(resp_msg)

    def send_update_route_info_ack(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x0C
        logger.info('send_update_route_info_ack')
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)

    def recv_set_brightness(self, msg_obj: TTIABusStopMessage):
        logger.info(f"recv_set_brightness: {msg_obj.payload.to_dict()}")
        self.estop.LightSet = msg_obj.payload.LightSet
        resp_msg = self.create_defaule_msg(0x0E)
        self.send_set_brightness_ack(resp_msg)

    def send_set_brightness_ack(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x0E
        logger.info('send_set_brightness_ack')
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)

    def recv_reboot(self, msg_obj: TTIABusStopMessage):
        logger.info(f"recv_reboot: {msg_obj.payload.to_dict()}")
        msg = self.create_defaule_msg(0x11)
        self.send_reboot_ack(msg)
        logger.info("do some reboot...")

    def send_reboot_ack(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x11
        logger.info('send_reboot_ack')
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)

    def recv_update_gif(self, msg_obj: TTIABusStopMessage):
        logger.info(f"recv_update_gif: {msg_obj.payload.to_dict()} \n {msg_obj.option_payload.to_dict()}")
        resp_msg = self.create_defaule_msg(0x12)
        self.send_update_gif_ack(resp_msg)

    def send_update_gif_ack(self, msg_obj: TTIABusStopMessage):
        assert msg_obj.header.MessageID == 0x12
        logger.info('send_update_gif_ack')
        self.sock.sendto(msg_obj.to_pdu(), self.server_addr)