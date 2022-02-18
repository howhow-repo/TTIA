from datetime import datetime, timedelta
from .ttiastopudpserver import TTIAStopUdpServer
from ..db_control import EStopObjCacher, MsgCacher
from ..TTIA_stop_message import TTIABusStopMessage
from ..StopMsg import StopMsg
import logging

logger = logging.getLogger(__name__)


def remove_job_by_msg(stop_msg: StopMsg):
    stop_ids = EStopObjCacher.get_stop_id_by_msg_group_id(stop_msg.gid)
    jobs = MsgCacher.scheduler.get_jobs()

    for job in jobs:
        job_id = job.id.split("_")

        if job_id[0] == 'MSG' and job_id[1] != 'default':
            if int(job_id[1]) == stop_msg.id:
                job.remove()

        if job_id[0] == 'MSG' and job_id[1] == 'default':
            if int(job_id[2]) in stop_ids:
                job.remove()


class TTIAAutomationServer:
    def __init__(self, sql_config, msg_scheduler, udp_server: TTIAStopUdpServer):
        self.udp_server = udp_server
        EStopObjCacher(sql_config).load_from_sql()
        MsgCacher(sql_config, msg_scheduler).load_from_sql()
        self.init_msg_jods()

    def init_msg_jods(self):
        for stop_msg in MsgCacher.msg_cache.values():
            self.__set_update_job(stop_msg)
            self.__set_expire_job(stop_msg)

    def reload_msg(self):
        old_msgs, new_msgs = MsgCacher.reload_from_sql()
        if len(old_msgs) > 0:
            for msg in old_msgs:
                remove_job_by_msg(msg)
        if len(new_msgs) > 0:
            for msg in new_msgs:
                self.__set_update_job(msg)
                self.__set_expire_job(msg)

    def update_msg_tag(self, msg_obj: TTIABusStopMessage):
        try:
            ack = self.udp_server.send_update_msg_tag(msg_obj=msg_obj, wait_for_resp=True)
            if not ack:
                raise ConnectionError(f"Fail to update stop {msg_obj.header.StopID} msg id {msg_obj.payload.MsgNo}")
        except Exception as e:
            logger.error(f"{e}")

    def __set_update_job(self, stop_msg: StopMsg):
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
            MsgCacher.scheduler.add_job(
                id=f"MSG_{stop_msg.id}_{stop_id}",
                func=self.update_msg_tag,
                args=(msg,),
                next_run_time=updatetime,
                max_instances=1,
            )

    def __set_expire_job(self, stop_msg: StopMsg):
        ids = EStopObjCacher.get_stop_id_by_msg_group_id(stop_msg.gid)
        for stop_id in ids:
            estop = EStopObjCacher.get_estop_by_id(stop_id)
            msg = TTIABusStopMessage(0x05, 'default')
            msg.header.StopID = stop_id
            msg.payload.MsgTag = 5
            msg.payload.MsgNo = estop.MsgNo
            msg.payload.MsgContent = estop.IdleMessage
            MsgCacher.scheduler.add_job(
                id=f"MSG_default_{stop_id}",
                func=self.update_msg_tag,
                args=(msg,),
                next_run_time=stop_msg.expiretime,
                max_instances=1,
            )

    def reload_stop_and_route(self):
        updated_route_stop = EStopObjCacher.reload_from_sql()
        for stop_id in updated_route_stop:
            self.send_route_info(stop_id)

    def reload_stop_and_route_by_ids(self, ids: list):
        updated_route_stop = EStopObjCacher.reload_from_sql_by_estop_ids(ids)
        for stop_id in updated_route_stop:
            self.send_route_info(stop_id)

    def send_route_info(self, stop_id: int):
        for seq, info in enumerate(EStopObjCacher.estop_cache[stop_id].routelist):
            msg = info.to_ttia(stop_id=stop_id, seq=seq)
            ack = self.udp_server.send_update_route_info(msg_obj=msg, wait_for_resp=True)
