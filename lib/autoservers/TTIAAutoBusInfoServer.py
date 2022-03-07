import threading
from datetime import datetime
from lib.udp_server.ttiastopudpserver import TTIAStopUdpServer
from lib.db_control import BusInfoCacher, EStopObjCacher
from lib.TTIA_stop_message import TTIABusStopMessage
import logging

logger = logging.getLogger(__name__)


class TTIAAutoBusInfoServer:
    def __init__(self, udp_server: TTIAStopUdpServer):
        BusInfoCacher().load_from_web()
        self.fail_update_stops = 0
        self.udp_server = udp_server

    def reload_bus_info(self):
        start_time = datetime.now()
        logger.info("Starting reload bus info....")

        changed_routes = BusInfoCacher.reload_from_web()

        all_thread = []
        job_num = 0
        self.fail_update_stops = 0
        for route_id, routestop_ids in changed_routes.items():
            for routestop_id in routestop_ids:
                msg = BusInfoCacher.businfo_cache[int(route_id)].to_ttia(int(routestop_id))

                while len(all_thread) > 1000:  # keep thread num under 1000. Don't crash the memory :)
                    [all_thread.remove(t) for t in all_thread if not t.is_alive()]

                thread = threading.Thread(target=self.send_bus_info, args=(msg, True))
                thread.start()
                job_num += 1
                all_thread.append(thread)

        # wait all thread done, log the result.
        for t in all_thread:
            t.join()

        # for logging
        changed_stops = []
        for stops in changed_routes.values():
            changed_stops += stops
        logger.info(f"len of changed_stops: {len(changed_stops)}")
        logger.info(
            f"Finish sending {job_num}s bus info update. -- time spent: {(datetime.now() - start_time).seconds} sec")
        if self.fail_update_stops > 0:
            logger.info(f"fail updating bus info to stops: {self.fail_update_stops}s")

    def send_bus_info(self, msg_obj: TTIABusStopMessage, wait_for_resp=True):
        try:
            self.udp_server.send_update_bus_info(msg_obj, wait_for_resp)
        except Exception as e:
            logger.debug(e)
            self.fail_update_stops += 1
