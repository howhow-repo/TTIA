import sys
from datetime import datetime
import requests
from decouple import config
from ..TTIA_stop_message import TTIABusStopMessage
from ..db_control import EStopObjCacher
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',)
logger = logging.getLogger(__name__)


def get_sid(rsid):
    sid = EStopObjCacher.rsid_sid_table.get(rsid)
    if not sid:
        sid = 0
    return sid


def get_seq(sid, rsid):
    estop = EStopObjCacher.estop_cache.get(sid)
    if not estop:
        return 0
    for route_info in estop.routelist:
        if route_info.rsid == rsid:
            return route_info.seqno
    return 0


def create_last_left_msg(StopID: int, RouteID: int):
    msg = TTIABusStopMessage(0x07, 'default')
    msg.header.StopID = StopID
    msg.payload.RouteID = RouteID
    msg.payload.IsLastBus = 1
    msg.payload.Direction = 3
    msg.option_payload.SpectialEstimateTime = 3
    msg.option_payload.MsgCContent = "末班車已過"
    msg.option_payload.MsgEContent = "LAST LEFT"
    return msg


def create_no_bus_msg(StopID: int, RouteID: int):
    msg = TTIABusStopMessage(0x07, 'default')
    msg.header.StopID = StopID
    msg.payload.RouteID = RouteID
    msg.payload.Direction = 2
    msg.option_payload.SpectialEstimateTime = 4
    msg.option_payload.MsgCContent = "今日未營運"
    msg.option_payload.MsgEContent = "NO BUS TODAY"
    return msg


class WebStop:
    def __init__(self, json_info: dict):
        self.bno = json_info.get('bno')  # a list
        if self.bno:
            self.bno = sorted(self.bno, key=lambda k: k['no'])  # sort bno by 'no'

        # est: estimate time (sec)
        if json_info.get('schTm'):
            self.est = json_info.get('schTm')
        elif json_info.get('schBus'):
            self.est = json_info.get('schBus')

        self.schBus = json_info.get('schBus')
        self.cdsec = json_info.get('cdsec')
        self.cdcnt = json_info.get('cdcnt')
        self.sid = json_info.get('sid')
        self.seq = json_info.get('seq')
        self.nm = json_info.get('nm')
        self.d = json_info.get('d')
        self.x = json_info.get('x')
        self.y = json_info.get('y')
        self.websid = json_info.get('websid')
        self.traveltime = json_info.get('traveltime')

    def to_json(self):
        return self.__dict__


class WebRoute:
    def __init__(self, json_info: dict):
        self.id = json_info.get('id')
        self.vid = json_info.get('vid')
        self.nm = json_info.get('nm')
        self.gopoints = json_info.get('gopoints')
        self.backpoints = json_info.get('backpoints')
        self.depart = json_info.get('depart')
        self.edepart = json_info.get('edepart')
        self.dest = json_info.get('dest')
        self.edest = json_info.get('edest')
        self.cars = json_info.get('cars')
        self.stops = {}  # actually is rsid
        if json_info.get('stops').items():
            self.stops = {int(stop_id): WebStop(stop) for stop_id, stop in json_info.get('stops').items()}

        max_seq = 0
        self.last_stop_id = 0
        for stop_id, stop in self.stops.items():
            if stop.seq == 1:
                self.first_stop_id = stop_id
            if stop.seq > max_seq:
                max_seq = stop.seq
                self.last_stop_id = stop_id

    def to_json(self):
        r = self.__dict__
        stops_json = {}
        for stop_id, stop in r['stops'].items():
            stops_json[str(stop_id)] = stop.to_json()
        r['stops'] = stops_json
        return r

    def to_ttia(self, routestop_id: int) -> TTIABusStopMessage:
        """return a TTIA msg obj with WRONG STOPID"""
        # sampled data
        web_stop = self.stops.get(routestop_id)
        sid = get_sid(routestop_id)
        if web_stop and web_stop.est != 'LAST LEFT' and web_stop.est != 'NO BUS':
            no_bus = False
        else:
            no_bus = True

        # init msg
        msg = TTIABusStopMessage(0x07, 'default')
        now = datetime.now()
        if no_bus:
            if web_stop.est == 'LAST LEFT':  # 末班車駛離
                msg = create_last_left_msg(RouteID=self.id, StopID=sid)
            elif web_stop.est == 'NO BUS':  # 今日未營運
                msg = create_no_bus_msg(RouteID=self.id, StopID=sid)

        else:  # 有車
            msg = TTIABusStopMessage(0x07, 'default')
            msg.header.StopID = sid
            msg.payload.RouteID = self.id
            if ":" in web_stop.est and web_stop.bno is None:  # 未發車
                schtime = datetime(now.year, now.month, now.day, int(web_stop.est.split(":")[0]), int(web_stop.est.split(":")[1]))
                msg.payload.EstimateTime = (schtime - now).seconds
                msg.option_payload.SpectialEstimateTime = 1
                msg.option_payload.MsgCContent = web_stop.est + ' 發車'
                msg.option_payload.MsgEContent = web_stop.est + " depot"

            elif web_stop.bno and web_stop.cdsec >= 180:  # 車在路上
                bus_info = web_stop.bno[0]
                msg.payload.CurrentStop = bus_info["sid"]
                msg.payload.DestinationStop = self.last_stop_id
                msg.payload.EstimateTime = web_stop.cdsec
                if web_stop.cdcnt > 0:
                    msg.payload.StopDistance = web_stop.cdcnt
                msg.option_payload.MsgCContent = f"余 {round(web_stop.cdsec // 60)} 分鐘"
                msg.option_payload.MsgEContent = f"Arr {round(web_stop.cdsec // 60)} min"

            elif web_stop.bno and 180 > web_stop.cdsec >= 60:  # 車在路上 & 即將進站
                bus_info = web_stop.bno[0]
                msg.payload.CurrentStop = bus_info["sid"]
                msg.payload.DestinationStop = self.last_stop_id
                msg.payload.EstimateTime = web_stop.cdsec
                if web_stop.cdcnt > 0:
                    msg.payload.StopDistance = web_stop.cdcnt
                msg.option_payload.MsgCContent = f"即將進站"
                msg.option_payload.MsgEContent = f"Nearly arr"

            elif web_stop.bno and 60 > web_stop.cdsec:  # 車在路上 & 進站中
                bus_info = web_stop.bno[0]
                msg.payload.CurrentStop = bus_info["sid"]
                msg.payload.DestinationStop = self.last_stop_id
                msg.payload.EstimateTime = web_stop.cdsec
                if web_stop.cdcnt > 0:
                    msg.payload.StopDistance = web_stop.cdcnt
                msg.option_payload.MsgCContent = f"車輛進站中"
                msg.option_payload.MsgEContent = f"Bus arriving"

        msg.payload.TransYear, msg.payload.TransMonth, msg.payload.TransDay, msg.payload.TransHour, msg.payload.TransMin, msg.payload.TransSec \
            = now.year, now.month, now.day, now.hour, now.minute, now.second
        msg.payload.RcvYear, msg.payload.RcvMonth, msg.payload.RcvDay, msg.payload.RcvHour, msg.payload.RcvMin, msg.payload.RcvSec \
            = now.year, now.month, now.day, now.hour, now.minute, now.second

        msg.option_payload.Sequence = get_seq(sid, routestop_id)
        return msg


class BusInfoCacher:
    source_host = config('BUS_INFO_SOURCE', cast=str, default='http://110.25.88.242:60001/api/v1/routes/')
    businfo_cache = {}
    # businfo_cache = {<route_id: int>: <WebRoute: obj>, <route_id: int>: <WebRoute: obj>, ....}

    @classmethod
    def load_from_web(cls):
        logger.info(f"Initing bus info from {cls.source_host}....")
        now = datetime.now()
        routeests = requests.get(cls.source_host, timeout=5).json()
        logger.debug(f"Getting bus info api time spend {(datetime.now() - now).seconds} sec, size: {sys.getsizeof(routeests)} Byte")
        for route_id, route in routeests.items():  # pack to obj
            cls.businfo_cache[int(route_id)] = WebRoute(route)
        logger.info(f"Init bus info success.")

    @classmethod
    def reload_from_web(cls) -> dict:
        """
            Reload data from source_host.
                1. update dict cache of bus info.
                2. return the ids of those data has been changed
            :return
            Updated routestop_ids pack with route id
            {
                <route_id: int>: [<routestop_id: int>, <routestop_id: int>, <routestop_id: int>...],
                <route_id: int>: [<routestop_id: int>, <routestop_id: int>, <routestop_id: int>...],
                ...
            }
        """
        updated_routes = {}  # {<route id>: [<stop_id>, <stop_id>,...], <route id>: [<stop_id>, <stop_id>,...],...}
        try:
            new_data = requests.get(cls.source_host, timeout=5).json()
        except Exception as e:
            logger.error(f"Reload BusInfoCacher from web fail. {e}")
            return {}

        for route_id, route in new_data.items():
            new_route_obj = WebRoute(route)
            old_route_obj = cls.businfo_cache.get(int(route_id))

            if old_route_obj:
                for stop_id, stop in new_route_obj.stops.items():
                    old_stop = old_route_obj.stops.get(int(stop_id))
                    if old_stop and old_stop.cdsec == stop.cdsec:
                        pass
                    else:
                        if route_id not in updated_routes:
                            updated_routes[route_id] = []
                        updated_routes[route_id].append(stop_id)
                        cls.businfo_cache[int(route_id)].stops[int(stop_id)] = stop
            else:  # no old_route
                updated_routes[route_id] = [stop.sid for stop in new_route_obj.stops]
        return updated_routes
        #  {
        #       <route_id>: [<stop_id>, <stop_id>, <stop_id>...],
        #       <route_id>: [<stop_id>, <stop_id>, <stop_id>...],
        #       ...
        #  }
