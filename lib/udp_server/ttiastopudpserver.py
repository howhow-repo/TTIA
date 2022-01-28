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

        if estop and msg_obj.header.StopID == estop.StopID:
            payload_dict = estop.to_dict()
            payload_dict['Result'] = 1
            payload_dict['MsgTag'] = 0
            payload_dict['BootTime'] = time(0, 0, 0)  # TODO: data from sql is define wired. Force overwrite.
            payload_dict['ShutdownTime'] = time(0, 0, 0)  # TODO: data from sql is define wired. Force overwrite.
            resp_msg.payload.from_lazy_dict(payload_dict)

        elif msg_obj.header.StopID != estop.StopID:
            logger.error("Fail to match data: StopID & IMSI does not match")

        self.sock.sendto(resp_msg.to_pdu(), section.client_addr)
        section.logs.append(resp_msg.header.MessageID)

    def recv_registration_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """
        # 基本資料程序確認訊息
        """
        if 1 not in section.logs:  # registration_check should go after do_registration
            self.wrong_communicate_order(section)
            return
        if msg_obj.payload.MsgStatus == 1:  # 訊息設定成功
            EStopObjCacher.estop_cache[msg_obj.header.StopID].ready = True
            EStopObjCacher.update_addr(msg_obj.header.StopID, section.client_addr)
            logger.info("registration check ok")

        elif msg_obj.payload.MsgStatus != 1:  # 訊息設定失敗
            logger.error("estop return fail in registration")

        self.remove_from_sections(section.stop_id)

    def recv_period_report(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """ 接收定時回報訊息 0x03 """
        print(f"0x03 period report recv from stop: {msg_obj.header.StopID}")
        print(msg_obj.to_dict())
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        if estop and estop.ready:
            estop.address = section.client_addr
            estop.SentCount = msg_obj.payload.SentCount
            estop.RecvCount = msg_obj.payload.RecvCount
            estop.lasttime = datetime.now()

            resp_msg = TTIABusStopMessage(0x04, 'default')
            self.sock.sendto(resp_msg.to_pdu(), section.client_addr)
        self.remove_from_sections(section.stop_id)

    def recv_abnormal(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        """ 接收定時回報訊息 0x09 """
        print("get abnormal report")
        print(msg_obj.to_dict())
        resp_msg = TTIABusStopMessage(0x0A, 'default')
        estop = EStopObjCacher.get_estop_by_id(msg_obj.header.StopID)
        if estop:
            estop.abnormal_log.append(msg_obj.payload)
            resp_msg.payload.MsgStatus = 1
        else:
            resp_msg.payload.MsgStatus = 0

        self.sock.sendto(resp_msg.to_pdu(), section.client_addr)