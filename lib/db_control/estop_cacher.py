import logging
from .mysql_handler import check_config_items
from .station_center import StationCenter
from ..EStop import EStop

logger = logging.getLogger(__name__)


class EStopObjCacher:
    """
        estop_cache data:
        {<StopID: int>:{<estop obj>}, <StopID: int>:{<estop obj>},....}
    """
    estop_cache = {}
    rsid_sid_table = {}
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
        cls.rsid_sid_table = cls.station.get_rsid_sid_table()
        cls.station.disconnect()

        cls.__pack_come_in_data(estops_dict)

    @classmethod
    def reload_from_sql_by_estop_ids(cls, ids: list):
        cls.station.connect()
        new_dict = cls.station.get_e_stop_by_ids(ids)
        cls.rsid_sid_table = cls.station.get_rsid_sid_table()
        cls.station.disconnect()

        route_updated_stops = []
        for estop_id in new_dict:
            old_stop = cls.estop_cache.get(estop_id)
            new_stop_dict = new_dict[estop_id]

            if old_stop:
                # Check new coming item is same as old item
                for key in new_stop_dict:
                    if new_stop_dict[key] == old_stop.to_dict()[key]:
                        continue
                    else:
                        logger.info(f"find diff at stop [{old_stop.StopID}]>> "
                                    f"{key}: {old_stop.to_dict()[key]} -> {new_stop_dict[key]}")
                        if key == 'routelist':
                            route_updated_stops.append(old_stop.StopID)
            else:
                estop_obj = EStop(new_stop_dict)
                cls.estop_cache[estop_obj.StopID] = estop_obj
                logger.info(f"Find new stop id {old_stop.StopID}, add to cache.")

        logger.info('reload stop done.')
        logger.debug(f'route_updated_stops: {route_updated_stops}')
        return set(route_updated_stops)

    @classmethod
    def reload_from_sql(cls):
        """
            Check if the new data same as the cache.
        """
        cls.station.connect()
        new_dict = cls.station.get_e_stops()
        cls.station.disconnect()

        route_updated_stops = []
        for estop_id in new_dict:
            old_stop = cls.estop_cache.get(estop_id)
            new_stop_dict = new_dict[estop_id]

            if old_stop:
                # Check new coming item is same as old item
                for key in new_stop_dict:
                    if new_stop_dict[key] == old_stop.to_dict()[key]:
                        continue
                    else:
                        logger.info(f"find diff at stop [{old_stop.StopID}]>> "
                                    f"{key}: {old_stop.to_dict()[key]} -> {new_stop_dict[key]}")
                        if key == 'routelist':
                            route_updated_stops.append(old_stop.StopID)
            else:
                estop_obj = EStop(new_stop_dict)
                cls.estop_cache[estop_obj.StopID] = estop_obj
                logger.info(f"Find new stop id {old_stop.StopID}, add to cache.")

        logger.info('reload stop done.')
        logger.debug(f'route_updated_stops: {route_updated_stops}')
        return set(route_updated_stops)

    @classmethod
    def __pack_come_in_data(cls, new_dict: dict):
        """Create new estop_obj or update estop_obj from sql data."""
        for estop_id in new_dict:
            estop_obj = EStop(new_dict[estop_id])
            if estop_obj.StopID in cls.estop_cache:
                cls.estop_cache[estop_id].from_dict(new_dict[estop_id])
            else:
                cls.estop_cache[estop_id] = estop_obj

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
    def get_estop_by_id(cls, id) -> EStop:
        return cls.estop_cache.get(int(id))

    @classmethod
    def get_estop_by_imsi(cls, imsi) -> EStop:
        for estop in cls.estop_cache.values():
            if estop.IMSI == imsi:
                return estop
        return None

    @classmethod
    def get_stop_id_by_msg_group_id(cls, group_id):
        ids = []
        for estop in cls.estop_cache.values():
            if estop.MessageGroupID == group_id:
                ids.append(estop.StopID)
        return ids
