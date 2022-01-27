from .mysql_handler import check_config_items
from .station_center import StationCenter
from ..estop import EStop


class EStopObjCacher:
    estop_cache = {}
    station = None

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
    def load_from_sql_by_estop_ids(cls, ids: list):
        cls.station.connect()
        estops_dict = cls.station.get_e_stop_by_id(ids)
        cls.station.disconnect()

        cls.__pack_come_in_data(estops_dict)

    @classmethod
    def __pack_come_in_data(cls, new_dict: dict):
        for es in new_dict:
            es_obj = EStop(new_dict[es])
            if es_obj.StopID in cls.estop_cache:
                cls.estop_cache[es].from_dict(new_dict[es])
            else:
                cls.estop_cache[es] = es_obj

    @classmethod
    def update_addr(cls, stop_id: int, addr):
        cls.update_info(stop_id, 'address', addr)

    @classmethod
    def update_info(cls, stop_id: int, prop_name: str, payload):
        if stop_id in cls.estop_cache:
            cls.estop_cache[stop_id].__setattr__(prop_name, payload)

    @classmethod
    def erase_cache(cls):
        cls.estop_cache = {}

    @classmethod
    def get_estop_by_imsi(cls, imsi) -> EStop:
        for estop in cls.estop_cache.values():
            if estop.IMSI == imsi:
                return estop
        return None
