from .base_server import UDPServer
from decouple import config
from lib import TTIABusStopMessage
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import logging


logger = logging.getLogger(__name__)
TIMEZONE = config('TIMEZONE', default="Asia/Taipei")


def decode_msg(data):
    try:
        return TTIABusStopMessage(data, 'pdu')
    except AssertionError:
        return False


class UDPWorkingSection:
    lifetime = 15  # second

    def __init__(self, stop_id, client_addr, msg_obj: TTIABusStopMessage):
        self.client_addr = client_addr
        self.stop_id = stop_id
        self.start_time = datetime.now()
        self.process_id = msg_obj.header.MessageID
        self.logs = {}  # self.logs = {<header.Sequence: int>: [<msg_obj>, <msg_obj>....],...}

    def to_json(self):
        self_dict = self.__dict__
        logs_json = {}
        for Sequence, msg_obj_list in self.logs.items():
            logs_json[Sequence] = [msg_obj.to_dict() for msg_obj in msg_obj_list]
        self_dict['logs'] = logs_json
        return self_dict


class SectionServer(UDPServer):
    section_lifetime = UDPWorkingSection.lifetime
    sections = {}
    routine_scheduler = BackgroundScheduler(timezone=TIMEZONE)

    def __init__(self, host, port):
        super().__init__(host, port)
        self.routine_scheduler.add_job(
            func=self.expire_timeout_section,
            trigger='interval',
            id='expire_timeout_section',
            seconds=self.section_lifetime / 2
        )
        self.routine_scheduler.start()

    @classmethod
    def expire_timeout_section(cls):
        now = datetime.now()
        should_be_del = []
        for section_id in cls.sections:
            if (now - cls.sections[section_id].start_time).seconds > UDPWorkingSection.lifetime:
                should_be_del.append(section_id)
        for section_id in should_be_del:
            del cls.sections[section_id]

    @classmethod
    def get_section(cls, stop_id):
        """
        :return:
            :return section if section is found
            :return None if section not found
        """
        for section_id in cls.sections:
            if section_id == stop_id:
                return cls.sections[section_id]
        return None

    @classmethod
    def create_new_section(cls, stop_id: int, client_address, msg_obj: TTIABusStopMessage):
        section = UDPWorkingSection(stop_id, client_address, msg_obj)
        cls.sections[stop_id] = section
        return section

    @classmethod
    def remove_from_sections(cls, stop_id):
        logger.debug(f"remove_from_sections: {stop_id}")
        if cls.sections.get(stop_id):
            del cls.sections[stop_id]

    @classmethod
    def remove_from_logs(cls, stop_id: int, seq: int):
        section = cls.sections.get(stop_id)
        if section:
            if section.logs.get(seq):
                del section.logs[seq]

    def handle_request(self, data, client_address):
        msg_obj = decode_msg(data)
        if not msg_obj:  # quick fail if data not ttia format
            return

        section = self.get_section(msg_obj.header.StopID)

        if not section:
            section = self.create_new_section(msg_obj.header.StopID, client_address, msg_obj)
            self.handle_new_section(msg_obj, section)

        else:  # old section
            self.handle_old_section(msg_obj, section)

    def handle_new_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        raise NotImplementedError

    def handle_old_section(self, msg_obj: TTIABusStopMessage, section: UDPWorkingSection):
        raise NotImplementedError

    def wrong_communicate_order(self, section: UDPWorkingSection):
        logger.debug(f"Wong communicate order. expire section of stop id: {section.stop_id}")
        self.remove_from_sections(section.stop_id)

    def unaccepted_cmd(self, section: UDPWorkingSection):
        logger.debug(f"Command unaccepted. expire section of stop id: {section.stop_id}")
        self.remove_from_sections(section.stop_id)
