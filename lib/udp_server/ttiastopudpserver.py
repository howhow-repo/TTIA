import threading
from .core import ServerSideHandler
from .core import UDPWorkingSection
from ..db_control import EStopObjCacher, MsgCacher
from ..TTIA_stop_message import TTIABusStopMessage
from datetime import datetime
import time as sys_time
import logging

logger = logging.getLogger(__name__)


def get_seq(sid, rsid):
    estop = EStopObjCacher.estop_cache.get(sid)
    if not estop:
        return 0
    for route_info in estop.routelist:
        if route_info.rsid == rsid:
            return route_info.seqno
    return 0


class TTIAStopUdpServer(ServerSideHandler):
    header_sequence = 1

    def __init__(self, host, port, timeout: int = 5):
        self.estop_comm_timeout = timeout
        super().__init__(host, port)

    @classmethod
    def add_header_seq(cls, msg_obj: TTIABusStopMessage):
        msg_obj.header.Sequence = cls.header_sequence
        cls.header_sequence += 1
        if cls.header_sequence > 65535:
            cls.header_sequence = 1
        return msg_obj

    def recv_registration(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """
        基本資料程序查詢註冊
        """
        logger.info(f"Start registration for stop id: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")
        resp_msg = TTIABusStopMessage(1, 'default')
        resp_msg.payload.Result = 0
        estop = EStopObjCacher.get_estop_by_imsi(msg_obj.payload.IMSI)

        if estop:
            if msg_obj.header.StopID == estop.StopID:
                payload_dict = estop.to_dict()
                payload_dict['Result'] = 1
                payload_dict['MsgTag'] = 0
                # payload_dict['BootTime'] = time(0, 0, 0)  # TODO: data from sql is define wired. Force overwrite.
                # payload_dict['ShutdownTime'] = time(0, 0, 0)  # TODO: data from sql is define wired. Force overwrite.
                resp_msg.payload.from_lazy_dict(payload_dict)
            else:
                logger.error("Fail to match data: StopID & IMSI does not match")

        else:
            logger.error("Can not find estop by given IMSI")
        self.send_registration_info(resp_msg, section)

    def send_registration_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x01
        logger.info("send_registration_info")
        msg_obj = self.add_header_seq(msg_obj)
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)

    def recv_registration_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """
        # 基本資料程序確認訊息
        """
        logger.info(f"recv_registration_ack: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

        if not section.logs.get(msg_obj.header.Sequence) and section.logs.get(msg_obj.header.Sequence)[
            -1].header.MessageID != 1:
            self.wrong_communicate_order(section, msg_obj.header.Sequence)
            return

        if msg_obj.payload.MsgStatus == 1:  # 訊息設定成功
            EStopObjCacher.estop_cache[msg_obj.header.StopID].ready = True
            EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
            EStopObjCacher.update_addr(msg_obj.header.StopID, section.client_addr)
            logger.info(f"id {msg_obj.header.StopID} registration ack ok")
            self.update_route_info(section.stop_id)
            self.update_msg(section.stop_id)

        else:  # 訊息設定失敗
            logger.warning(f"estop {msg_obj.header.StopID} return fail in registration")
        self.remove_from_logs(msg_obj.header.StopID, msg_obj.header.Sequence)

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
        msg_obj = self.add_header_seq(msg_obj)
        msg_obj.header.StopID = section.stop_id
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)
        self.remove_from_logs(msg_obj.header.StopID, msg_obj.header.Sequence)
        logger.debug(f"send_period_report_ack: {msg_obj.header.StopID} ")

    def send_update_msg_tag(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        msg_obj = self.add_header_seq(msg_obj)
        assert msg_obj.header.MessageID == 0x05
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.get_section(msg_obj.header.StopID)
        if not section:
            section = self.create_new_section(msg_obj.header.StopID, estop.address)
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_update_msg_tag: {msg_obj.header.StopID} ")

        if wait_for_resp:
            ack = self.wait_ack(section, msg_obj.header.Sequence, 0x06)
            while resend > 0 and ack is None:
                logger.info("resending msg_tag...")
                resend -= 1
                self.sock.sendto(msg_obj.to_pdu(), estop.address)
                ack = self.wait_ack(section, msg_obj.header.Sequence, 0x06)
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return ack
        else:
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return

    def recv_update_msg_tag_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_update_msg_tag_ack from id: {msg_obj.header.StopID}")

    def send_update_bus_info(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        msg_obj = self.add_header_seq(msg_obj)
        assert msg_obj.header.MessageID == 0x07
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop, f"Can not find client {msg_obj.header.StopID}"
        assert estop.ready, f"Client {msg_obj.header.StopID} is not ready yet."
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.get_section(msg_obj.header.StopID)
        if not section:
            section = self.create_new_section(msg_obj.header.StopID, estop.address)
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_update_bus_info: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

        if wait_for_resp:
            ack = self.wait_ack(section, msg_obj.header.Sequence, 0x08)
            while resend > 0 and ack is None:
                logger.info("resending bus_info...")
                resend -= 1
                self.sock.sendto(msg_obj.to_pdu(), estop.address)
                ack = self.wait_ack(section, msg_obj.header.Sequence, 0x08)
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return ack
        else:
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return

    def recv_update_bus_info_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_update_bus_ack from id: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

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
        msg_obj = self.add_header_seq(msg_obj)
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)
        self.remove_from_logs(msg_obj.header.StopID, msg_obj.header.Sequence)

    def send_update_route_info(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        msg_obj = self.add_header_seq(msg_obj)
        assert msg_obj.header.MessageID == 0x0B, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.get_section(msg_obj.header.StopID)
        if not section:
            section = self.create_new_section(msg_obj.header.StopID, estop.address)
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_update_route_info: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

        if wait_for_resp:
            ack = self.wait_ack(section, msg_obj.header.Sequence, 0x0C)
            while resend > 0 and ack is None:
                logger.info("resending route_info...")
                resend -= 1
                self.sock.sendto(msg_obj.to_pdu(), estop.address)
                ack = self.wait_ack(section, msg_obj.header.Sequence, 0x0C)
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return ack
        else:
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return

    def recv_update_route_info_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_update_route_info_ack from id: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

    def send_set_brightness(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        msg_obj = self.add_header_seq(msg_obj)
        assert msg_obj.header.MessageID == 0x0D, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.get_section(msg_obj.header.StopID)
        if not section:
            section = self.create_new_section(msg_obj.header.StopID, estop.address)
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_set_brightness: {msg_obj.header.StopID} ")

        if wait_for_resp:
            ack = self.wait_ack(section, msg_obj.header.Sequence, 0x0E)
            while resend > 0 and ack is None:
                logger.info("resending set_brightness...")
                resend -= 1
                self.sock.sendto(msg_obj.to_pdu(), estop.address)
                ack = self.wait_ack(section, msg_obj.header.Sequence, 0x0E)
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return ack
        else:
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return

    def recv_set_brightness_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_set_brightness from id: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

    def send_reboot(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        msg_obj = self.add_header_seq(msg_obj)
        assert msg_obj.header.MessageID == 0x10, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.get_section(msg_obj.header.StopID)
        if not section:
            section = self.create_new_section(msg_obj.header.StopID, estop.address)
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_reboot: {msg_obj.header.StopID} ")

        if wait_for_resp:
            ack = self.wait_ack(section, msg_obj.header.Sequence, 0x11)
            while resend > 0 and ack is None:
                logger.info("resending reboot...")
                resend -= 1
                self.sock.sendto(msg_obj.to_pdu(), estop.address)
                ack = self.wait_ack(section, msg_obj.header.Sequence, 0x11)
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return ack
        else:
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return

    def recv_reboot_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_reboot_ack from id: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

    def send_update_gif(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        msg_obj = self.add_header_seq(msg_obj)
        assert msg_obj.header.MessageID == 0x12, "uncorrect message id"
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        assert estop.address is not None, f"Can not find client {msg_obj.header.StopID} address"
        section = self.get_section(msg_obj.header.StopID)
        if not section:
            section = self.create_new_section(msg_obj.header.StopID, estop.address)
        section.logs[msg_obj.header.Sequence] = [msg_obj]
        self.sock.sendto(msg_obj.to_pdu(), estop.address)
        logger.info(f"send_update_gif: {msg_obj.header.StopID} ")
        if wait_for_resp:
            ack = self.wait_ack(section, msg_obj.header.Sequence, 0x13)
            while resend > 0 and ack is None:
                logger.info("resending update_gif...")
                resend -= 1
                self.sock.sendto(msg_obj.to_pdu(), estop.address)
                ack = self.wait_ack(section, msg_obj.header.Sequence, 0x13)
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return ack
        else:
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            return

    def recv_update_gif_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        EStopObjCacher.estop_cache[msg_obj.header.StopID].lasttime = datetime.now()
        logger.info(f"recv_update_gif_ack from id: {msg_obj.header.StopID}, {msg_obj.header.Sequence}")

    def wait_ack(self, section: UDPWorkingSection, seq: int, expected_msg_id: int):
        check_interval = 0.5
        for i in range(int(self.estop_comm_timeout / check_interval)):
            if section.logs[seq][-1].header.MessageID == expected_msg_id:
                ack_msg = section.logs[seq][-1]
                self.remove_from_logs(section.stop_id, seq)
                return ack_msg
            else:
                sys_time.sleep(check_interval)
        logger.warning(
            f"Did not get ack from client {section.stop_id}, seq: {seq}, expected_msg_id: {expected_msg_id}.")
        return None

    def update_route_info(self, stop_id: int):
        estop = EStopObjCacher.get_estop_by_id(stop_id)
        if estop:
            for i, route in enumerate(estop.routelist):
                msg = route.to_ttia(stop_id, i)
                thread = threading.Thread(target=self.send_update_route_info, args=(msg, True, 3))
                thread.start()
            logger.info(f"{len(estop.routelist)}s route_ids has been sent.")

    def update_msg(self, stop_id: int):
        estop = EStopObjCacher.estop_cache.get(stop_id)
        if estop:
            gid = estop.MessageGroupID
            stop_msg = MsgCacher.get_msg_by_group_id(gid)
            if stop_msg and stop_msg.updatetime < datetime.now() < stop_msg.expiretime:
                msg = stop_msg.to_ttia(stop_id)
                self.send_update_msg_tag(msg)
