import logging
from datetime import datetime
from .section_server import SectionServer, UDPWorkingSection
from lib import TTIABusStopMessage

logger = logging.getLogger(__name__)


def add_to_section_log(msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
    if msg_obj.header.Sequence != 0:
        if section.logs.get(msg_obj.header.Sequence):
            section.logs[msg_obj.header.Sequence].append(msg_obj)
        else:
            section.logs[msg_obj.header.Sequence] = [msg_obj]


class ServerSideHandler(SectionServer):
    header_sequence = 1

    def __init__(self, host, port):
        super().__init__(host, port)

    @classmethod
    def add_header_seq(cls, msg_obj: TTIABusStopMessage):
        msg_obj.header.Sequence = cls.header_sequence
        cls.header_sequence += 1
        if cls.header_sequence > 65535:
            cls.header_sequence = 1
        return msg_obj

    def handle_new_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        add_to_section_log(msg_obj, section)

        if msg_obj.header.MessageID == 0x00:  # 基本資料程序
            self.recv_registration(msg_obj, section)
        elif msg_obj.header.MessageID == 0x03:  # 定時回報程序
            self.recv_period_report(msg_obj, section)
        elif msg_obj.header.MessageID == 0x09:  # 異常回報
            self.recv_abnormal(msg_obj, section)
        elif msg_obj.header.MessageID == 0x11:  # 重開通知訊息 TODO: 重開通知訊息能夠單向發送？
            self.recv_reboot_ack(msg_obj, section)

        # """ 異常處理 """
        elif msg_obj.header.MessageID in [0x01, 0x05, 0x07, 0x0B, 0x0D, 0x10, 0x12]:
            # client 不可對server做設定。
            self.unaccepted_cmd(section, msg_obj.header.Sequence)
        elif msg_obj.header.MessageID in [0x02, 0x06, 0x08, 0x0C, 0x0E, 0x13]:
            # client 非預期回覆
            self.wrong_communicate_order(section, msg_obj.header.Sequence)

        elif msg_obj.header.MessageID in [0x04, 0x0A]:
            # 應由server端發出的訊息
            self.wrong_communicate_order(section, msg_obj.header.Sequence)

        else:
            logger.warning("drop new_section unknown message id.")
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            self.sock.sendto(b"echo: unknown msg id\n", section.client_addr)

    def handle_old_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        section.last_msg_time = datetime.now()
        add_to_section_log(msg_obj, section)

        if msg_obj.header.MessageID == 0x02:  # 基本資料程序ack
            self.recv_registration_ack(msg_obj, section)
        elif msg_obj.header.MessageID == 0x06:  # 更新站牌文字ack
            self.recv_update_msg_tag_ack(msg_obj, section)
        elif msg_obj.header.MessageID == 0x08:  # 更新公車資訊ack
            self.recv_update_bus_info_ack(msg_obj, section)
        elif msg_obj.header.MessageID == 0x0C:  # 更新路線資訊ack
            self.recv_update_route_info_ack(msg_obj, section)
        elif msg_obj.header.MessageID == 0x0E:  # 更新亮度ack
            self.recv_set_brightness_ack(msg_obj, section)
        elif msg_obj.header.MessageID == 0x13:  # 更新gif ack
            self.recv_update_gif_ack(msg_obj, section)

        # """ 異常處理 """

        elif msg_obj.header.MessageID in [0x01, 0x05, 0x07, 0x0B, 0x0D, 0x10, 0x12]:
            # client 不可對server做設定。
            self.unaccepted_cmd(section, msg_obj.header.Sequence)

        elif msg_obj.header.MessageID in [0x00, 0x03, 0x09, 0x11]:
            # 新工作項目
            self.handle_new_section(msg_obj, section)

        elif msg_obj.header.MessageID in [0x04, 0x0A]:
            # 應由server端發出的訊息
            self.wrong_communicate_order(section, msg_obj.header.Sequence)

        else:
            logger.warning("drop old_section unknown message id.")
            self.remove_from_logs(section.stop_id, msg_obj.header.Sequence)
            self.sock.sendto(b"echo: unknown msg id\n", section.client_addr)

    # TTIA estop behaviors
    def recv_registration(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x00
        raise NotImplementedError

    def send_registration_info(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x01
        raise NotImplementedError

    def recv_registration_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x02
        raise NotImplementedError

    def recv_period_report(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x03
        raise NotImplementedError

    def send_period_report_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x04
        raise NotImplementedError

    def send_update_msg_tag(self, msg_obj: TTIABusStopMessage):  # 0x05
        raise NotImplementedError

    def recv_update_msg_tag_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x06
        raise NotImplementedError

    def send_update_bus_info(self, msg_obj: TTIABusStopMessage):  # 0x07
        raise NotImplementedError

    def recv_update_bus_info_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x08
        raise NotImplementedError

    def recv_abnormal(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x09
        raise NotImplementedError

    def send_abnormal_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0A
        raise NotImplementedError

    def send_update_route_info(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def recv_update_route_info_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError

    def send_set_brightness(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def recv_set_brightness_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError

    def send_reboot(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def recv_reboot_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError

    def send_update_gif(self, msg_obj: TTIABusStopMessage):  # 0x0B
        raise NotImplementedError

    def recv_update_gif_ack(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):  # 0x0C
        raise NotImplementedError
