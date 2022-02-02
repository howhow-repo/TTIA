from .mysql_handler import MySqlHandler
from datetime import time


def pack_e_stop_data(dict_like_data):
    if "BootTime" in dict_like_data.keys():
        BootTime = str(dict_like_data['BootTime']).zfill(6)
        time_str = [int(BootTime[i:i + 2]) for i in range(0, len(BootTime), 2)]
        # split str every 2 char
        dict_like_data['BootTime'] = time((time_str[0]), time_str[1], time_str[2])

    if "ShutdownTime" in dict_like_data.keys():
        ShutdownTime = str(dict_like_data['ShutdownTime']).zfill(6)
        print("ShutdownTime: ", ShutdownTime)
        time_str = [int(ShutdownTime[i:i + 2]) for i in range(0, len(ShutdownTime), 2)]
        # split str every 2 char
        dict_like_data['ShutdownTime'] = time(time_str[0], time_str[1], time_str[2])

    e_stop_data_template = {
        "StopID": dict_like_data["id"],
        "IMSI": dict_like_data["imsi"],
        "StopCName": dict_like_data["name"],
        "StopEName": dict_like_data["ename"],
        "MessageGroupID": dict_like_data["gid"],
        "BootTime": dict_like_data["boottime"],
        "ShutdownTime": dict_like_data["shutdowntime"],
        "IdleMessage": dict_like_data["idlemessage"],
        "DisplayMode": dict_like_data["displaymode"],
        "TextRollingSpeed": dict_like_data["textrollingspeed"],
        "DistanceFunctionMode": dict_like_data["distancefunctionmode"],
        "ReportPeriod": dict_like_data["reportperiod"],
        'TypeID': dict_like_data["tid"],
        'Provider': dict_like_data["vid"],
        'Latitude': dict_like_data["lat"],
        'Longitude': dict_like_data["lon"],
        'routelist': []
    }
    return e_stop_data_template


def pack_route_data(dict_like_data):
    routelist_template = {
        "rrid": dict_like_data["rrid"],
        "sid": dict_like_data["sid"],
        "gid": dict_like_data["gid"],
        "dir": dict_like_data["dir"],
        "seqno": dict_like_data["seqno"],
        "rname": dict_like_data["rname"],
        "rename": dict_like_data["rename"],
    }
    return routelist_template


class StationCenter(MySqlHandler):
    """
        'host', 'port', 'user', 'password', 'db'
        should be included in mysql_config
    """
    def __init__(self, mysql_config: dict):
        super().__init__(mysql_config)

    def get_e_stops(self):
        """
            return a dict with estops's info as format below:
            {
                <stop_id: int>:{
                    "id": <stop_id>,
                    ... ,
                    ...(some stop configs)...,
                    ... ,

                    "routelist":[
                        {...(some route info)...},
                        {...(some route info)...}.
                        ...
                    ]
                },
                ...
                <multiple stops>
                ...

            }
        """

        cmd = """
            SELECT 
                estop.id AS id,
                estop.imsi AS imsi,
                estop.name AS name,
                estop.gid AS gid,
                estop.ename,
                estop.boottime,
                estop.shutdowntime,
                estop.idlemessage,
                estop.displaymode,
                estop.textrollingspeed,
                estop.distancefunctionmode,
                estop.reportperiod,
                estop.lat AS lat,
                estop.lon AS lon,
                routestop.rid AS rrid,
                routestop.id AS sid,
                routestop.seqno AS seqno,
                routestop.direction AS dir,
                route.name AS rname,
                route.ename AS `rename`,
                estop.tid AS tid,
                estop.vid AS vid
            FROM
                estop
                    LEFT JOIN
                estoproutes ON estop.id = estoproutes.esid
                    LEFT JOIN
                routestop ON estoproutes.ssid = routestop.id
                    LEFT JOIN
                route ON routestop.rid = route.id
            ORDER BY id
        """

        raw_data = self._get_table_in_dict(cmd)
        e_stops_dict = {}
        for s in raw_data:
            if s['id'] not in e_stops_dict:
                e_stops_dict.update({s['id']: pack_e_stop_data(s)})
            e_stops_dict[s['id']]['routelist'].append(pack_route_data(s))

        return e_stops_dict

    def get_e_stop_by_id(self, ids: list):
        """
            return like get_e_stop, but with data only stop_ids that requested.
        """
        ids = tuple(ids)
        condition = ''
        if len(ids) > 0:
            if len(ids) == 1:
                condition = f' where estop.id = {ids[0]} '
            else:
                condition = f' where estop.id IN {ids} '

        cmd = f"""
            SELECT 
                estop.id AS id,
                estop.imsi AS imsi,
                estop.name AS name,
                estop.gid AS gid,
                estop.ename,
                estop.boottime,
                estop.shutdowntime,
                estop.idlemessage,
                estop.displaymode,
                estop.textrollingspeed,
                estop.distancefunctionmode,
                estop.reportperiod,
                estop.lat AS lat,
                estop.lon AS lon,
                routestop.rid AS rrid,
                routestop.id AS sid,
                routestop.seqno AS seqno,
                routestop.direction AS dir,
                route.name AS rname,
                route.ename AS 'rename',
                estop.tid AS tid,
                estop.vid AS vid
            FROM
                estop
                    LEFT JOIN
                estoproutes ON estop.id = estoproutes.esid
                    LEFT JOIN
                routestop ON estoproutes.ssid = routestop.id
                    LEFT JOIN
                route ON routestop.rid = route.id
                {condition}
            ORDER BY id
        """
        raw_data = self._get_table_in_dict(cmd)
        e_stops_dict = {}
        for s in raw_data:
            if s['id'] not in e_stops_dict:
                e_stops_dict.update({s['id']: pack_e_stop_data(s)})
            e_stops_dict[s['id']]['routelist'].append(pack_route_data(s))

        return e_stops_dict
