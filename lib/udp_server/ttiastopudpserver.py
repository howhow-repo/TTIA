from .serversidehandler import ServerSideHandler
from .section_server import UDPWorkingSection
from lib import EStopObjCacher, TTIABusStopMessage
from datetime import datetime, time
import logging


logger = logging.getLogger(__name__)


class TTIAStopUdpServer(ServerSideHandler):

    def __init__(self, host, port):
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
            print("err")
            logger.error("Fail to get estop by imsi")
        self.send_registration_info(resp_msg, section)

    def send_registration_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x01
        logger.info("send_registration_info")
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)
        section.logs.append(msg_obj.header.MessageID)

    def recv_registration_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """
        # 基本資料程序確認訊息
        """
        logger.info("recv_registration_check")
        if 1 not in section.logs:  # registration_check should go after do_registration
            self.wrong_communicate_order(section)
            return

        if msg_obj.payload.MsgStatus == 1:  # 訊息設定成功
            EStopObjCacher.estop_cache[msg_obj.header.StopID].ready = True
            EStopObjCacher.update_addr(msg_obj.header.StopID, section.client_addr)
            logger.info(f"id {msg_obj.header.StopID} registration check ok")

        else:  # 訊息設定失敗
            logger.warning(f"estop {msg_obj.header.StopID} return fail in registration")

        self.remove_from_sections(section.stop_id)

    def recv_period_report(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """ 接收定時回報訊息 0x03 """
        logger.info(f"period report recv from stop: {msg_obj.header.StopID}")
        resp_msg = TTIABusStopMessage(0x04, 'default')
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        if estop:
            estop.address = section.client_addr
            estop.ready = True
            estop.SentCount = msg_obj.payload.SentCount
            estop.RevCount = msg_obj.payload.RevCount
            estop.lasttime = datetime.now()

        self.send_period_report_check(resp_msg, section)

    def send_period_report_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)
        self.remove_from_sections(section.stop_id)

    def send_update_msg_tag(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        assert msg_obj.header.MessageID == 0x05
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)

    def recv_update_msg_tag_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        logger.info(f"recv_update_msg_tag_check from id: {msg_obj.header.StopID}")

    def send_update_bus_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        assert msg_obj.header.MessageID == 0x07
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)

    def recv_update_bus_info_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        logger.info(f"recv_update_msg_tag_check from id: {msg_obj.header.StopID}")

    def recv_abnormal(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """ 接收定時回報訊息 0x09 """
        logger.warning("get abnormal report: ", msg_obj.to_dict())
        resp_msg = TTIABusStopMessage(0x0A, 'default')
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        if estop:
            estop.abnormal_log.append(msg_obj.payload)
            resp_msg.payload.MsgStatus = 1
        else:
            resp_msg.payload.MsgStatus = 0

        self.send_abnormal_check(resp_msg, section)

    def send_abnormal_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        self.sock.sendto(msg_obj.to_pdu(), section.client_addr)
        self.remove_from_sections(section.stop_id)


