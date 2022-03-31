from lib.udp_server.ttiastopudpserver import TTIAStopUdpServer
from lib.db_control import EStopObjCacher
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',)
logger = logging.getLogger(__name__)


class TTIAAutoStopAndRouteServer:
    def __init__(self, sql_config: dict, udp_server: TTIAStopUdpServer):
        EStopObjCacher(sql_config).load_from_sql()
        self.udp_server = udp_server

    def reload_stop_and_route(self):
        updated_route_stop = EStopObjCacher.reload_from_sql()
        for stop_id in updated_route_stop:
            self.udp_server.update_route_info(stop_id)

    def reload_stop_and_route_by_ids(self, ids: list):
        updated_route_stop = EStopObjCacher.reload_from_sql_by_estop_ids(ids)
        for stop_id in updated_route_stop:
            self.udp_server.update_route_info(stop_id)

    @classmethod
    def check_online(cls):
        """if miss two Period Report, set ready to false"""
        logger.debug("checking stop online...")
        for estop in EStopObjCacher.estop_cache.values():
            if estop.ready and estop.lasttime:
                now = datetime.now()
                delta_time = now - estop.lasttime
                if delta_time > timedelta(seconds=estop.ReportPeriod * 2):
                    estop.ready = False
                    estop.offline_log.append(now)
                    logger.error(f"set estop {estop.StopID} ready = False: {delta_time.seconds} seconds not replied.")

    @classmethod
    def remove_timeout_log(cls):
        """Remove the timeout logs from online/offline in EStop """
        pass
