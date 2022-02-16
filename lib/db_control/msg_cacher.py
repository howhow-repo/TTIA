from datetime import datetime, timedelta
import logging
from .mysql_handler import check_config_items
from .station_center import StationCenter
from apscheduler.schedulers.background import BackgroundScheduler
from ..udp_server.ttiastopudpserver import TTIAStopUdpServer
from ..TTIA_stop_message import TTIABusStopMessage
from .estop_cacher import EStopObjCacher
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
    ttia_server = TTIAStopUdpServer

    @classmethod
    def __init__(cls, mysql_config: dict, scheduler: BackgroundScheduler, ttia_server: TTIAStopUdpServer):
        cls.scheduler = scheduler
        cls.ttia_server = ttia_server
        check_config_items(mysql_config)
        try:
            cls.station = StationCenter(mysql_config=mysql_config)
        except Exception as err:
            raise ConnectionError(f"Can not init mysql database. \n {err}")

    @classmethod
    def load_from_sql(cls):
        cls.station.connect()
        estops_dict = cls.station.get_valid_msgs()
        cls.station.disconnect()

        cls.__pack_come_in_data(estops_dict)

    @classmethod
    def reload_from_sql(cls):
        """
            Check if the new data same as the cache.

            do nothing if nochange;
            add jod if new msg;
            del old job and readd job if updated.
        """
        cls.station.connect()
        estops_dict = cls.station.get_valid_msgs()
        cls.station.disconnect()

        for msg_dict in estops_dict:
            msg_tag = StopMsg().from_dict(msg_dict)
            old_msg = cls.msg_cache.get(msg_tag.id)

            if old_msg and old_msg.__dict__ == msg_tag.__dict__:
                continue
            else:
                logger.info(f"Find msg id {msg_tag.id} is updated, add update schedule.")
                cls.__remove_job_by_msg(old_msg)
                cls.__set_update_job(msg_tag)
                cls.__set_expire_job(msg_tag)
                cls.msg_cache[msg_tag.id] = msg_tag

    @classmethod
    def init_msg_jods(cls):
        cls.scheduler.remove_all_jobs()
        """
            Set msg send job to scheduler.
            if updatetime < now < expiretime, job will fire after 120 seconds.
            else, job will fire on update time.

        """
        for stop_msg in cls.msg_cache.values():
            cls.__set_update_job(stop_msg)
            cls.__set_expire_job(stop_msg)

    @classmethod
    def send_update_msg_tag(cls, msg_obj: TTIABusStopMessage):
        try:
            ack = cls.ttia_server.send_update_msg_tag(msg_obj=msg_obj, wait_for_resp=True)
            if not ack:
                raise ConnectionError(f"Fail to update stop {msg_obj.header.StopID} msg id {msg_obj.payload.MsgNo}")
        except Exception as e:
            logger.error(f"{e}")

    @classmethod
    def __pack_come_in_data(cls, new_dict: dict):
        """overwrite msg."""
        for msg_dict in new_dict:
            msg_tag = StopMsg().from_dict(msg_dict)
            cls.msg_cache[msg_tag.id] = msg_tag

    @classmethod
    def __set_update_job(cls, stop_msg: StopMsg):
        ids = EStopObjCacher.get_stop_id_by_msg_group_id(stop_msg.gid)
        for stop_id in ids:
            msg = TTIABusStopMessage(0x05, 'default')
            msg.header.StopID = stop_id
            msg.payload.MsgTag = stop_msg.tagid
            msg.payload.MsgNo = stop_msg.id
            msg.payload.MsgContent = stop_msg.msg
            if stop_msg.updatetime < datetime.now():
                updatetime = datetime.now() + timedelta(seconds=120)
            else:
                updatetime = stop_msg.updatetime

            cls.scheduler.add_job(
                id=f"MSG_{stop_msg.id}_{stop_id}",
                func=cls.send_update_msg_tag,
                args=(msg,),
                next_run_time=updatetime,
                max_instances=1,
            )


    @classmethod
    def __set_expire_job(cls, stop_msg: StopMsg):
        ids = EStopObjCacher.get_stop_id_by_msg_group_id(stop_msg.gid)
        for stop_id in ids:
            estop = EStopObjCacher.get_estop_by_id(stop_id)
            msg = TTIABusStopMessage(0x05, 'default')
            msg.header.StopID = stop_id
            msg.payload.MsgTag = 5
            msg.payload.MsgNo = estop.MsgNo
            msg.payload.MsgContent = estop.IdleMessage

            cls.scheduler.add_job(
                id=f"MSG_default_{stop_id}",
                func=cls.send_update_msg_tag,
                args=(msg,),
                next_run_time=stop_msg.expiretime,
                max_instances=1,
            )

    @classmethod
    def __remove_job_by_msg(cls, stop_msg: StopMsg):
        stop_ids = EStopObjCacher.get_stop_id_by_msg_group_id(stop_msg.gid)
        jobs = cls.scheduler.get_jobs()

        for job in jobs:
            job_id = job.id.split("_")

            if job_id[0] == 'MSG' and job_id[1] != 'default':
                if int(job_id[1]) == stop_msg.id:
                    job.remove()

            if job_id[0] == 'MSG' and job_id[1] == 'default':
                if int(job_id[2]) in stop_ids:
                    job.remove()

