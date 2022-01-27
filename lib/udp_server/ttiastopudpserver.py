from .base_server import UDPServer, UDPWorkingSection
from lib import EStopObjCacher, TTIABusStopMessage
from datetime import datetime, time
import logging


logger = logging.getLogger(__name__)


def decode_msg(data):
    try:
        return TTIABusStopMessage(data, 'pdu')
    except AssertionError:
        return False


class TTIAStopUdpServer(UDPServer):

    def __init__(self, host, port):
        super().__init__(host, port)

    def handle_request(self, data, client_address):
        msg_obj = decode_msg(data)
        if not msg_obj:  # quick fail if data not ttia format
            return

        section = self.section_or_none(msg_obj.header.StopID)

        if not section:
            section = UDPWorkingSection(msg_obj.header.StopID, client_address, msg_obj.header.MessageID)
            self.sections[msg_obj.header.StopID] = section
            self.handle_new_section(msg_obj, section)

        else:  # old section
            self.handle_old_section(msg_obj, section)

    def handle_new_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        if msg_obj.header.MessageID == 0x00:  # 基本資料程序
            self.do_registration(msg_obj, section)
        elif msg_obj.header.MessageID == 0x02:  # 基本資料程序
            self.wrong_section_order(section)
        elif msg_obj.header.MessageID == 0x03:  # 定時回報程序
            self.recv_period_report()
        else:
            print("drop new_section unknown message id.")
            self.remove_from_sections(section.stop_id)
            self.sock.sendto(b"echo: unknown msg id\n", section.client_addr)

    def handle_old_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        section.start_time = datetime.now()
        if msg_obj.header.MessageID == 0x00:  # 基本資料程序
            self.wrong_section_order(section)

        elif msg_obj.header.MessageID == 0x02:  # 基本資料程序
            self.do_registration_check(msg_obj, section)
        else:
            logger.error("drop old_section unknown message id.")
            self.remove_from_sections(msg_obj.header.StopID)
            self.sock.sendto(b"echo: unknown msg id\n", section.client_addr)

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
            self.wrong_section_order(section)
            return
        if msg_obj.payload.MsgStatus == 1:  # 訊息設定成功
            EStopObjCacher.estop_cache[msg_obj.header.StopID].ready = True
            print("registration check ok")
        elif msg_obj.payload.MsgStatus != 1:  # 訊息設定失敗
            logger.error("estop return fail in registration")
        self.remove_from_sections(section.stop_id)

    def recv_period_report(self):  # 定時回報程序
        # TODO
        pass

    def wrong_section_order(self, section: UDPWorkingSection ):
        logger.error("exist section with wong section order.")
        self.remove_from_sections(section.stop_id)
