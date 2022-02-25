from lib.udp_server.ttiastopudpserver import TTIAStopUdpServer
from lib.db_control import EStopObjCacher
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class TTIAAutoStopAndRouteServer:
    def __init__(self, sql_config: dict, udp_server: TTIAStopUdpServer):
        EStopObjCacher(sql_config).load_from_sql()
        self.udp_server = udp_server

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

    @classmethod
    def check_online(cls):
        """if miss two Period Report, set ready to false"""
        logger.debug("checking stop online...")
        for estop in EStopObjCacher.estop_cache.values():
            if estop.ready and estop.lasttime:
                delta_time = datetime.now() - estop.lasttime
                if delta_time > timedelta(seconds=estop.ReportPeriod * 2):
                    estop.ready = False
                    logger.warning(f"set estop {estop.StopID} ready = False: {delta_time.seconds} seconds not replied.")
