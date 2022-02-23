from .core import ServerSideHandler
from .core import UDPWorkingSection
from ..db_control import EStopObjCacher
from ..TTIA_stop_message import TTIABusStopMessage
from datetime import datetime, time
import time as systime
import time as sys_time
import logging

logger = logging.getLogger(__name__)


class TTIAStopUdpServer(ServerSideHandler):

    def __init__(self, host, port, timeout: int = 5):
        self.estop_comm_timeout = timeout
        super().__init__(host, port)

    def recv_registration(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """
        基本資料程序查詢註冊
        """
        logger.info(f"Start registration for stop id: {msg_obj.header.StopID}")
        resp_msg = TTIABusStopMessage(1, 'default')
        resp_msg.payload.Result = 0
        estop = EStopObjCacher.get_estop_by_imsi(msg_obj.payload.IMSI)

        if estop:
            if msg_obj.header.StopID == estop.StopID:
                payload_dict = estop.to_dict()
                payload_dict['Result'] = 1
                payload_dict['MsgTag'] = 0
                payload_dict['BootTime'] = time(0, 0, 0)  # TODO: data from sql is define wired. Force overwrite.
                payload_dict['ShutdownTime'] = time(0, 0, 0)  # TODO: data from sql is define wired. Force overwrite.
                resp_msg.payload.from_lazy_dict(payload_dict)
            else:
                logger.error("Fail to match data: StopID & IMSI does not match")

        else:
            logger.error("Can not find estop by given IMSI")
        self.send_registration_info(resp_msg, section)

    def send_registration_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x01
        logger.info("send_registration_info")
        section.logs.append(msg_obj)
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)

    def recv_registration_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """
        # 基本資料程序確認訊息
        """
        logger.info("recv_registration_ack")
        if section.logs[-2].header.MessageID != 1:  # registration_ack should go after do_registration
            self.wrong_communicate_order(section)
            return

        if msg_obj.payload.MsgStatus == 1:  # 訊息設定成功
            EStopObjCacher.estop_cache[msg_obj.header.StopID].ready = True
            EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
            EStopObjCacher.update_addr(msg_obj.header.StopID, section.client_addr)
            logger.info(f"id {msg_obj.header.StopID} registration ack ok")
            self.update_route_info(section.stop_id)

        else:  # 訊息設定失敗
            logger.warning(f"estop {msg_obj.header.StopID} return fail in registration")

        self.remove_from_sections(section.stop_id)

    def recv_period_report(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """ 接收定時回報訊息 0x03 """
        logger.debug(f"period report recv from stop: {msg_obj.header.StopID}")
        resp_msg = TTIABusStopMessage(0x04, 'default')
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        if estop:
            estop.address = section.client_addr
            estop.ready = True
            estop.SentCount = msg_obj.payload.SentCount
            estop.RevCount = msg_obj.payload.RevCount
            estop.lasttime = datetime.now()

        self.send_period_report_ack(resp_msg, section)

    def send_period_report_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        msg_obj.header.StopID = section.stop_id
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)
        self.remove_from_sections(section.stop_id)
        logger.debug(f"send_period_report_ack: {msg_obj.header.StopID} ")

    def send_update_msg_tag(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        assert msg_obj.header.MessageID == 0x05
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.create_new_section(msg_obj.header.StopID, estop.address, msg_obj)
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_update_msg_tag: {msg_obj.header.StopID} ")
        if wait_for_resp:
            return self.wait_ack(section, 0x06)
        else:
            return

    def recv_update_msg_tag_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_update_msg_tag_ack from id: {msg_obj.header.StopID}")

    def send_update_bus_info(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        assert msg_obj.header.MessageID == 0x07
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop, f"Can not find client {msg_obj.header.StopID}"
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.create_new_section(msg_obj.header.StopID, estop.address, msg_obj)
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        # logger.info(f"send_update_bus_info: {msg_obj.header.StopID} ")
        if wait_for_resp:
            return self.wait_ack(section, 0x08)
        else:
            return

    def recv_update_bus_info_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        # logger.info(f"recv_update_msg_tag_ack from id: {msg_obj.header.StopID}")

    def recv_abnormal(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """ 接收定時回報訊息 0x09 """
        logger.warning("get abnormal report: ", msg_obj.to_dict())
        resp_msg = TTIABusStopMessage(0x0A, 'default')
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        if estop:
            msg_obj.payload.set_Rcv_time(datetime.now())
            estop.abnormal_log.append(msg_obj.payload)
            resp_msg.payload.MsgStatus = 1
        else:
            resp_msg.payload.MsgStatus = 0

        self.send_abnormal_ack(resp_msg, section)

    def send_abnormal_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)
        self.remove_from_sections(section.stop_id)

    def send_update_route_info(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        assert msg_obj.header.MessageID == 0x0B, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.create_new_section(msg_obj.header.StopID, estop.address, msg_obj)
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_update_route_info: {msg_obj.header.StopID} ")
        if wait_for_resp:
            return self.wait_ack(section, 0x0C)
        else:
            return

    def recv_update_route_info_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_update_route_info_ack from id: {msg_obj.header.StopID}")

    def send_set_brightness(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        assert msg_obj.header.MessageID == 0x0D, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.create_new_section(msg_obj.header.StopID, estop.address, msg_obj)
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_set_brightness: {msg_obj.header.StopID} ")
        if wait_for_resp:
            return self.wait_ack(section, 0x0E)
        else:
            return

    def recv_set_brightness_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_set_brightness from id: {msg_obj.header.StopID}")

    def send_reboot(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        assert msg_obj.header.MessageID == 0x10, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.create_new_section(msg_obj.header.StopID, estop.address, msg_obj)
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_reboot: {msg_obj.header.StopID} ")
        if wait_for_resp:
            return self.wait_ack(section, 0x11)
        else:
            return

    def recv_reboot_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_reboot_ack from id: {msg_obj.header.StopID}")

    def send_update_gif(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        assert msg_obj.header.MessageID == 0x12, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.create_new_section(msg_obj.header.StopID, estop.address, msg_obj)
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_update_gif: {msg_obj.header.StopID} ")
        if wait_for_resp:
            return self.wait_ack(section, 0x13)
        else:
            return

    def recv_update_gif_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_update_gif_ack from id: {msg_obj.header.StopID}")

    def wait_ack(self, section: UDPWorkingSection, expected_msg_id: int):
        check_interval = 0.5
        for i in range(int(self.estop_comm_timeout / check_interval)):
            if section.logs[-1].header.MessageID == expected_msg_id:
                ack_msg = section.logs[-1]
                self.remove_from_sections(section.stop_id)
                return ack_msg
            else:
                sys_time.sleep(check_interval)
        logger.warning("do not get ack from client.")
        return None

    def update_route_info(self, stop_id: int):
        estop = EStopObjCacher.get_estop_by_id(stop_id)
        for i, route in enumerate(estop.routelist):
            msg = route.to_ttia(stop_id, i)
            ack = self.send_update_route_info(msg, wait_for_resp=True)

    def fake_udp_job(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        logger.info(f"sending fake udp msg... {msg_obj.header.StopID}")
        systime.sleep(2)
        logger.info(f"fake udp msg sent done. {msg_obj.header.StopID}")