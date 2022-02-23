from .station_center import StationCenter
from apscheduler.schedulers.background import BackgroundScheduler
from ..udp_server.ttiastopudpserver import TTIAStopUdpServer
from .mysql_handler import check_config_items
from ..RouteInfo import RouteInfo
from .estop_cacher import EStopObjCacher


class RouteCacher:
    """
    No Usage Now!!

     route_cache data:
        {<stop_id: int>:{<route_info obj>}, <stop_id: int>:{<route_info obj>},....}
    """
    route_cache = {}
    station = StationCenter
    scheduler = BackgroundScheduler
    ttia_server = TTIAStopUdpServer

    @classmethod
    def __init__(cls, mysql_config: dict):
        check_config_items(mysql_config)
        try:
            cls.station = StationCenter(mysql_config=mysql_config)
        except Exception as err:
            raise ConnectionError(f"Can not init mysql database. \n {err}")

    @classmethod
    def load_from_sql(cls):
        cls.station.connect()
        estops_dict = cls.station.get_e_stops()
        cls.station.disconnect()

        cls.__pack_come_in_data(estops_dict)

    @classmethod
    def reload_from_sql(cls):
        cls.station.connect()
        stop_dict = cls.station.get_e_stops()
        cls.station.disconnect()

        new_dict = {}
        for estop_id in stop_dict:
            routelist = []
            for route_info in stop_dict[estop_id]['routelist']:
                routelist.append(RouteInfo(route_info))
            new_dict[estop_id] = routelist

        not_same_stop = []
        for stop_id, info_list in new_dict.items():
            for i, new_info in enumerate(info_list):
                if new_info.to_dict() == cls.route_cache[stop_id][i].to_dict():
                    continue
                else:
                    not_same_stop.append(stop_id)
                    cls.route_cache[stop_id] = info_list
                    break
            if stop_id in not_same_stop:
                pass
                cls.route_cache[stop_id] = info_list
                EStopObjCacher.estop_cache[stop_id].routelist = info_list

        if len(not_same_stop) > 0:
            for id in not_same_stop:
                if EStopObjCacher.estop_cache[id].ready:
                    cls.send_route_info(id)


    @classmethod
    def __pack_come_in_data(cls, new_dict: dict):
        """Create new estop or update estop from sql data."""
        for estop_id in new_dict:
            routelist = []
            for route_info in new_dict[estop_id]['routelist']:
                routelist.append(RouteInfo(route_info))
            cls.route_cache[estop_id] = routelist

    @classmethod
    def send_route_info(cls, stop_id):
        for seq, info in enumerate(cls.route_cache[stop_id]):
            msg = info.to_ttia(stop_id=stop_id, seq=seq)
            ack = cls.ttia_server.send_update_route_info(msg_obj=msg, wait_for_resp=True)

