from datetime import datetime, timedelta

import requests
from decouple import config
from ..TTIA_stop_message import TTIABusStopMessage


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
        self.stops = {}
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

    def to_ttia(self, stop_id: int):
        # sampled data
        web_stop = self.stops.get(stop_id)
        if web_stop and web_stop.est != 'LAST LEFT' and web_stop.est != 'NO BUS':
            no_bus = False
        else:
            no_bus = True

        # init msg
        msg = TTIABusStopMessage(0x07, 'default')
        now = datetime.now()
        if no_bus:
            if web_stop.est == 'LAST LEFT':  # 末班車駛離
                msg = create_last_left_msg(RouteID=self.id, StopID=stop_id)
            elif web_stop.est == 'NO BUS':  # 今日未營運
                msg = create_no_bus_msg(RouteID=self.id, StopID=stop_id)

        else:
            msg = TTIABusStopMessage(0x07, 'default')
            msg.header.StopID = stop_id
            msg.payload.RouteID = self.id
            if ":" in web_stop.est and web_stop.bno is None: # TODO: 未發車
                schtime = datetime(now.year, now.month, now.day, web_stop.est.split(":")[0], web_stop.est.split(":")[1])
                msg.payload.EstimateTime = (schtime - now).seconds
                msg.option_payload.SpectialEstimateTime = 1
                msg.option_payload.MsgCContent = web_stop.est + ' 發車'
                msg.option_payload.MsgEContent = web_stop.est + " depot"

            elif web_stop.bno and web_stop.cdsec >= 180:  # TODO: 車在路上
                bus_info = web_stop.bno[0]
                msg.payload.CurrentStop = bus_info["sid"]
                msg.payload.DestinationStop = self.last_stop_id
                msg.payload.EstimateTime = web_stop.cdsec
                if web_stop.cdcnt > 0:
                    msg.payload.StopDistance = web_stop.cdcnt
                msg.option_payload.MsgCContent = f"尚余 {web_stop.cdsec//60} 分鐘進站"
                msg.option_payload.MsgEContent = f"Will be arrived after {web_stop.cdsec//60} min."

            elif web_stop.bno and 180 > web_stop.cdsec >= 60:  # TODO: 車在路上 & 即將進站
                bus_info = web_stop.bno[0]
                msg.payload.CurrentStop = bus_info["sid"]
                msg.payload.DestinationStop = self.last_stop_id
                msg.payload.EstimateTime = web_stop.cdsec
                if web_stop.cdcnt > 0:
                    msg.payload.StopDistance = web_stop.cdcnt
                msg.option_payload.MsgCContent = f"3分鐘內 即將進站"
                msg.option_payload.MsgEContent = f"Will be soon arrived within 3 min."

            elif web_stop.bno and 60 > web_stop.cdsec:  # TODO: 車在路上 & 進站中
                bus_info = web_stop.bno[0]
                msg.payload.CurrentStop = bus_info["sid"]
                msg.payload.DestinationStop = self.last_stop_id
                msg.payload.EstimateTime = web_stop.cdsec
                if web_stop.cdcnt > 0:
                    msg.payload.StopDistance = web_stop.cdcnt
                msg.option_payload.MsgCContent = f"車輛進站中..."
                msg.option_payload.MsgEContent = f"Bus arriving...."

        msg.payload.TransYear, msg.payload.TransMonth, msg.payload.TransDay, msg.payload.TransHour, msg.payload.TransMin, msg.payload.TransSec \
            = now.year, now.month, now.day, now.hour, now.minute, now.second
        msg.payload.RcvYear, msg.payload.RcvMonth, msg.payload.RcvDay, msg.payload.RcvHour, msg.payload.RcvMin, msg.payload.RcvSec \
            = now.year, now.month, now.day, now.hour, now.minute, now.second

        return msg


class WebStop:
    def __init__(self, json_info: dict):
        self.bno = json_info.get('bno')

        if json_info.get('schTm'):
            self.est = json_info.get('schTm')
        elif json_info.get('cdsec'):
            self.est = json_info.get('cdsec')
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


class BusInfoCacher:
    source_host = config('BUS_INFO_SOURCE', cast=str, default='http://110.25.88.242:60001/api/v1/routes/')
    businfo_cache = {}

    def load_from_web(self):
        routeests = requests.get(self.source_host, timeout=5).json()
        for route_id, route in routeests.items():  # pack to obj
            self.businfo_cache[int(route_id)] = WebRoute(route)

    def reload_from_web(self):
        """Reload data from source_host.
            :return
            a list of stop_id that data changes. Mostly is the bus info has changed.
        """
        updated_stops = []
        updated_routes = []
        new_data = requests.get(self.source_host, timeout=5).json()

        for route_id, route in new_data.items():
            new_route_obj = WebRoute(route)
            for stop_id, stop in new_route_obj.stops.items():
                old_stop = self.businfo_cache[int(route_id)].stops[int(stop_id)]
                if stop.to_json() == old_stop.to_json():
                    pass
                else:
                    updated_stops.append(stop_id)
                    updated_routes.append(route_id)
                    self.businfo_cache[int(route_id)].stops[int(stop_id)] = stop

        return set(updated_stops), set(updated_routes)
