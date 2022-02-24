import threading
import time
from queue import Queue
from datetime import datetime, timedelta
from .ttiastopudpserver import TTIAStopUdpServer
from ..db_control import EStopObjCacher, MsgCacher, BusInfoCacher
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
        self.fail_update_stops = 0
        self.udp_server = udp_server
        EStopObjCacher(sql_config).load_from_sql()
        MsgCacher(sql_config, msg_scheduler).load_from_sql()
        BusInfoCacher().load_from_web()
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

    def reload_bus_info(self):
        start_time = datetime.now()
        logger.info("Starting reload bus info....")

        changed_routes = BusInfoCacher.reload_from_web()
        changed_stops = []
        for stops in changed_routes.values():
            changed_stops += stops

        all_thread = []
        job_num = 0
        self.fail_update_stops = 0
        for route_id, stop_ids in changed_routes.items():
            for stop_id in stop_ids:
                msg = BusInfoCacher.businfo_cache[int(route_id)].to_ttia(int(stop_id))

                while len(all_thread) > 1000:  # keep thread num under 1000. Don't crash the memory :)
                    [all_thread.remove(t) for t in all_thread if not t.is_alive()]

                thread = threading.Thread(target=self.send_bus_info, args=(msg, True))
                thread.start()
                job_num += 1
                all_thread.append(thread)

        # wait all thread done, log the result.
        for t in all_thread:
            t.join()
        logger.info(f"len of changed_stops: {len(changed_stops)}")
        logger.info(f"Finish sending {job_num}s bus info update. -- time spent: {(datetime.now()-start_time).seconds} sec")
        if self.fail_update_stops > 0:
            logger.warning(f"fail updating stops: {self.fail_update_stops}s")

    def send_bus_info(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        try:
            self.udp_server.send_update_bus_info(msg_obj, wait_for_resp)
        except Exception as e:
            logger.debug(e)
            self.fail_update_stops += 1
