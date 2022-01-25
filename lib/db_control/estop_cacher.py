from .mysql_handler import check_config_items
from .station_center import StationCenter
from ..estop import EStop


class EStopObjCacher:
    estop_cache = {}
    station = None

    def __init__(self, mysql_config: dict):
        check_config_items(mysql_config)
        try:
            self.station = StationCenter(mysql_config=mysql_config)
        except Exception as err:
            raise ConnectionError(f"Can not init mysql database. \n {err}")

    def load_from_sql(self):
        self.station.connect()
        estops_dict = self.station.get_e_stops()
        self.station.disconnect()

        self.pack_come_in_data(estops_dict)

    def load_from_sql_by_estop_ids(self, ids: list):
        self.station.connect()
        estops_dict = self.station.get_e_stop_by_id(ids)
        self.station.disconnect()

        self.pack_come_in_data(estops_dict)

    def pack_come_in_data(self, new_dict: dict):
        for es in new_dict:
            es_obj = EStop(new_dict[es])
            if es_obj.StopID in self.estop_cache:
                self.estop_cache[es].update(es_obj)
            else:
                self.estop_cache[es] = es_obj

    def update_addr(self, stop_id: int, addr):
        self.update_info(stop_id, 'address', addr)

    def update_info(self, stop_id: int, prop_name: str, payload):
        if stop_id in self.estop_cache:
            self.estop_cache[stop_id].__setattr__(prop_name, payload)

    def erase_cache(self):
        self.estop_cache = {}
