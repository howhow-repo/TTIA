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
        self.all_threads = []
        self.fail_update_stops = 0
        self.udp_server = udp_server

    def limiting_threads(self):
        """keep thread num under 1000. Don't crash the memory :)"""
        while len(self.all_threads) > 1000:
            [self.all_threads.remove(t) for t in self.all_threads if not t.is_alive()]

    def reload_bus_info(self):
        start_time = datetime.now()
        logger.info("Starting reload bus info....")

        changed_routes = BusInfoCacher.reload_from_web()
        end_get_rawdata = datetime.now()

        job_num = 0
        self.fail_update_stops = 0

        start_sending_info_time = datetime.now()
        for route_id, routestop_ids in changed_routes.items():
            for routestop_id in routestop_ids:
                msg = BusInfoCacher.businfo_cache[int(route_id)].to_ttia(int(routestop_id))
                self.send_bus_info(msg_obj=msg, wait_for_resp=False)
                job_num += 1

        end_sending_info_time = datetime.now()

        # for logging
        changed_stops = []
        for stops in changed_routes.values():
            changed_stops += stops
        logger.info(f"len of changed_stops: {len(changed_stops)}")
        logger.info(f"Getting bus info api time spend {(end_get_rawdata - start_time).seconds} sec.")
        logger.info(f"sending udp time spend {(end_sending_info_time - start_sending_info_time).seconds} sec.")
        logger.info(
            f"Finish sending {job_num}s bus info update. -- time spent: {(datetime.now() - start_time).seconds} sec")

        if self.fail_update_stops > 0:
            logger.info(f"fail updating bus info to stops: {self.fail_update_stops}s")

    def send_bus_info(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        self.limiting_threads()
        thread = threading.Thread(target=self.send_bus_info_safe,
                                  args=(msg_obj, wait_for_resp, resend))
        thread.start()
        self.all_threads.append(thread)

    def send_bus_info_safe(self, msg_obj: TTIABusStopMessage, wait_for_resp: bool = True, resend: int = 0):
        # print(f"start thread of {msg_obj.header.StopID}-{msg_obj.payload.RouteID}")
        try:
            self.udp_server.send_update_bus_info(msg_obj, wait_for_resp, resend)
        except Exception as e:
            logger.debug(e)
            self.fail_update_stops += 1
        else:
            # print(f"end thread of {msg_obj.header.StopID}-{msg_obj.payload.RouteID}")
            pass
        finally:
            pass
            # print(f"end thread of {msg_obj.header.StopID}-{msg_obj.payload.RouteID}")

