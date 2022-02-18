from datetime import datetime, timedelta
import logging
from .mysql_handler import check_config_items
from .station_center import StationCenter
from apscheduler.schedulers.background import BackgroundScheduler
from ..StopMsg import StopMsg

logger = logging.getLogger(__name__)


class MsgCacher:
    """
        msg_cache data:
        {<msg_id: int>:{<estop obj>}, <StopID: int>:{<estop obj>},....}
    """
    msg_cache = {}
    station = None
    scheduler = BackgroundScheduler

    @classmethod
    def __init__(cls, mysql_config: dict, scheduler: BackgroundScheduler):
        cls.scheduler = scheduler
        check_config_items(mysql_config)
        try:
            cls.station = StationCenter(mysql_config=mysql_config)
        except Exception as err:
            raise ConnectionError(f"Can not init mysql database. \n {err}")

    @classmethod
    def load_from_sql(cls):
        estops_dict = cls.__get_new_dict()

        cls.__pack_come_in_data(estops_dict)

    @classmethod
    def reload_from_sql(cls):
        """
            Check if the new data same as the cache.

            :return
            list of changed msg
        """
        estops_dict = cls.__get_new_dict()

        changed_msg = []
        updated_msg = []
        for msg_dict in estops_dict:
            new_msg = StopMsg().from_dict(msg_dict)
            old_msg = cls.msg_cache.get(new_msg.id)

            if old_msg and old_msg.__dict__ == new_msg.__dict__:
                continue
            else:
                logger.info(f"Find msg id {new_msg.id} is updated, add update schedule.")
                changed_msg.append(old_msg)
                updated_msg.append(new_msg)
                cls.msg_cache[new_msg.id] = new_msg

        return changed_msg, updated_msg

    @classmethod
    def __pack_come_in_data(cls, new_dict: dict):
        """overwrite msg."""
        for msg_dict in new_dict:
            msg_tag = StopMsg().from_dict(msg_dict)
            cls.msg_cache[msg_tag.id] = msg_tag

    @classmethod
    def __get_new_dict(cls):
        cls.station.connect()
        estops_dict = cls.station.get_valid_msgs()
        cls.station.disconnect()
        return estops_dict
