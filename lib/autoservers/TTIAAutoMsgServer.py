from datetime import datetime, timedelta
from decouple import config
from lib.udp_server.ttiastopudpserver import TTIAStopUdpServer
from lib.db_control import EStopObjCacher, MsgCacher
from lib.TTIA_stop_message import TTIABusStopMessage
from apscheduler.schedulers.background import BackgroundScheduler
from lib.StopMsg import StopMsg
import logging


logger = logging.getLogger(__name__)


class TTIAAutoMsgServer:
    def __init__(self, udp_server: TTIAStopUdpServer):
        TIMEZONE = config('TIMEZONE', default="Asia/Taipei")
        self.udp_server = udp_server
        self.scheduler = BackgroundScheduler(timezone=TIMEZONE)
        self.init_msg_jods()

    def init_msg_jods(self):
        for stop_msg in MsgCacher.msg_cache.values():
            self.__set_update_job(stop_msg)
            self.__set_expire_job(stop_msg)

    def reload_msg(self):
        old_msgs, new_msgs = MsgCacher.reload_from_sql()
        if len(old_msgs) > 0:
            for msg in old_msgs:
                self.remove_job_by_msg(msg)
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

    def send_msg(self, stop_id: int):
        estop = EStopObjCacher.estop_cache.get(stop_id)
        if estop:
            gid = estop.MessageGroupID
            stop_msg = MsgCacher.get_msg_by_group_id(gid)
            if stop_msg and stop_msg.updatetime < datetime.now() < stop_msg.expiretime:
                msg = stop_msg.to_ttia(stop_id)
                ack = self.udp_server.send_update_msg_tag(msg)
        else:
            logger.error(f"estop {stop_id} not found.")

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
            self.scheduler.add_job(
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
            self.scheduler.add_job(
                id=f"MSG_default_{stop_id}",
                func=self.update_msg_tag,
                args=(msg,),
                next_run_time=stop_msg.expiretime,
                max_instances=1,
            )

    def remove_job_by_msg(self, stop_msg: StopMsg):
        stop_ids = EStopObjCacher.get_stop_id_by_msg_group_id(stop_msg.gid)
        jobs = self.scheduler.get_jobs()

        for job in jobs:
            job_id = job.id.split("_")

            if job_id[0] == 'MSG' and job_id[1] != 'default':
                if int(job_id[1]) == stop_msg.id:
                    job.remove()

            if job_id[0] == 'MSG' and job_id[1] == 'default':
                if int(job_id[2]) in stop_ids:
                    job.remove()