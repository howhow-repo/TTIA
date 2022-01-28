import logging
from datetime import datetime
from .section_server import SectionServer, UDPWorkingSection
from lib import TTIABusStopMessage

logger = logging.getLogger(__name__)


class ServerSideHandler(SectionServer):
    def __init__(self, host, port):
        super().__init__(host, port)

    def handle_new_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        if msg_obj.header.MessageID == 0x00:  # 基本資料程序
            self.recv_registration(msg_obj, section)
        elif msg_obj.header.MessageID == 0x03:  # 定時回報程序
            self.recv_period_report(msg_obj, section)
        elif msg_obj.header.MessageID == 0x09:  # 異常回報
            self.recv_abnormal(msg_obj, section)
        elif msg_obj.header.MessageID == 0x11:  # 重開通知訊息
            self.recv_reboot_check(msg_obj, section)

        # """ 異常處理 """

        elif msg_obj.header.MessageID in [0x01, 0x05, 0x07, 0x0B, 0x0D, 0x10, 0x12]:
            # client 不可對server做設定。
            self.unaccepted_cmd(section)
        elif msg_obj.header.MessageID in [0x02, 0x06, 0x0C, 0x0E, 0x13]:
            # client 非預期回覆
            self.wrong_communicate_order(section)

        elif msg_obj.header.MessageID in [0x04, 0x0A, 0x08]:
            # 應由server端發出的訊息
            self.wrong_communicate_order(section)

        else:
            print("drop new_section unknown message id.")
            self.remove_from_sections(section.stop_id)
            self.sock.sendto(b"echo: unknown msg id\n", section.client_addr)

    def handle_old_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        section.start_time = datetime.now()

        if msg_obj.header.MessageID == 0x02:  # 基本資料程序ok
            self.recv_registration_check(msg_obj, section)
        elif msg_obj.header.MessageID == 0x06:  # 更新站牌文字ok
            self.recv_update_msg_tag_check(msg_obj, section)
        elif msg_obj.header.MessageID == 0x0C:  # 更新站牌文字ok
            self.recv_update_route_info_check(msg_obj, section)
        elif msg_obj.header.MessageID == 0x0E:  # 更新站牌文字ok
            self.recv_set_brightness_check(msg_obj, section)
        elif msg_obj.header.MessageID == 0x13:  # 更新站牌文字ok
            self.recv_update_gif_check(msg_obj, section)

        # """ 異常處理 """

        elif msg_obj.header.MessageID in [0x01, 0x05, 0x07, 0x0B, 0x0D, 0x10, 0x12]:
            # client 不可對server做設定。
            self.unaccepted_cmd(section)

        elif msg_obj.header.MessageID in [0x00, 0x03, 0x09, 0x11]:
            # 新工作項目
            self.handle_new_section(msg_obj, section)

        elif msg_obj.header.MessageID in [0x04, 0x08, 0x0A]:
            # 應由server端發出的訊息
            self.wrong_communicate_order(section)

        else:
            logger.error("drop old_section unknown message id.")
            self.remove_from_sections(msg_obj.header.StopID)
            self.sock.sendto(b"echo: unknown msg id\n", section.client_addr)

    #### TTIA estop behaviors
    def recv_registration(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x00
        raise NotImplementedError

    def send_registration_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x01
        raise NotImplementedError

    def recv_registration_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x02
        raise NotImplementedError

    def recv_period_report(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x03
        raise NotImplementedError

    def send_period_report_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x04
        raise NotImplementedError

    def send_update_msg_tag(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x05
        raise NotImplementedError

    def recv_update_msg_tag_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x06
        raise NotImplementedError

    def send_update_bus_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x07
        raise NotImplementedError

    def recv_update_bus_info_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x08
        raise NotImplementedError

    def recv_abnormal(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x09
        raise NotImplementedError

    def recv_abnormal_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0A
        raise NotImplementedError

    def send_update_route_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0B
        raise NotImplementedError

    def recv_update_route_info_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError

    def send_set_brightness(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0B
        raise NotImplementedError

    def recv_set_brightness_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError

    def send_reboot(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0B
        raise NotImplementedError

    def recv_reboot_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError

    def send_update_gif(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0B
        raise NotImplementedError

    def recv_update_gif_check(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError