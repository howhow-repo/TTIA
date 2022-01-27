from .base_server import UDPServer, UDPWorkingSection
from .section_server import SectionServer
from lib import EStopObjCacher, TTIABusStopMessage
from datetime import datetime, time
import logging


logger = logging.getLogger(__name__)


class TTIAStopUdpServer(SectionServer):

    def __init__(self, host, port):
        super().__init__(host, port)

    def do_registration(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 基本資料程序
        print(f"start registration for stop id: {msg_obj.header.StopID}")
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

        self.sock.sendto(resp_msg.to_pdu(), section.client_addr)
        section.logs.append(resp_msg.header.MessageID)

    def do_registration_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 基本資料程序
        if section.logs[-1] != 1:  # registration_check should go after do_registration
            self.wrong_communicate_order(section)
            return
        if msg_obj.payload.MsgStatus == 1:  # 訊息設定成功
            EStopObjCacher.estop_cache[msg_obj.header.StopID].ready = True
            print("registration check ok")
        elif msg_obj.payload.MsgStatus != 1:  # 訊息設定失敗
            logger.error("estop return fail in registration")
        self.remove_from_sections(section.stop_id)

    def recv_period_report(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        pass
