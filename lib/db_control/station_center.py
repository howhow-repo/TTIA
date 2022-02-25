from .mysql_handler import MySqlHandler
from datetime import time

demo_cmd = """
                SELECT 
                stop.id AS id,
                stop.id AS imsi,
                stop.name AS name,
                stop.id AS gid,
                stop.ename,
                stop.lat AS lat,
                stop.lon AS lon,
                routestop.rid AS rid,
                routestop.id AS rsid,
                routestop.seqno AS seqno,
                routestop.direction AS dir,
                route.name AS rname,
                route.ename AS `rename`
            FROM
                stop
                    LEFT JOIN
                routestop ON stop.id = routestop.sid
                    LEFT JOIN
                route ON routestop.rid = route.id

"""


def pack_e_stop_data(dict_like_data):
    if "boottime" in dict_like_data.keys():
        BootTime = str(dict_like_data['boottime']).zfill(6)
        time_str = [int(BootTime[i:i + 2]) for i in range(0, len(BootTime), 2)]
        # split str every 2 char
        dict_like_data['boottime'] = time((time_str[0]), time_str[1], time_str[2])

    if "shutdowntime" in dict_like_data.keys():
        ShutdownTime = str(dict_like_data['shutdowntime']).zfill(6)
        time_str = [int(ShutdownTime[i:i + 2]) for i in range(0, len(ShutdownTime), 2)]
        # split str every 2 char
        dict_like_data['shutdowntime'] = time(time_str[0], time_str[1], time_str[2])

    if "reportperiod" in dict_like_data.keys():
        if dict_like_data['reportperiod'] == 0:
            dict_like_data['reportperiod'] = 60

    e_stop_data_template = {
        "StopID": dict_like_data.get("id"),
        "IMSI": str(dict_like_data.get("imsi")),
        "StopCName": dict_like_data.get("name"),
        "StopEName": dict_like_data.get("ename"),
        "MessageGroupID": dict_like_data.get("gid"),
        "BootTime": dict_like_data.get("boottime"),
        "ShutdownTime": dict_like_data.get("shutdowntime"),
        "IdleMessage": dict_like_data.get("idlemessage"),
        "DisplayMode": dict_like_data.get("displaymode"),
        "TextRollingSpeed": dict_like_data.get("textrollingspeed"),
        "DistanceFunctionMode": dict_like_data.get("distancefunctionmode"),
        "ReportPeriod": dict_like_data.get("reportperiod"),
        'TypeID': dict_like_data.get("tid"),
        'Provider': dict_like_data.get("vid"),
        'Latitude': dict_like_data.get("lat"),
        'Longitude': dict_like_data.get("lon"),
        'routelist': []
    }
    rm_k = []
    for k, v in e_stop_data_template.items():
        if v is None:
            rm_k.append(k)
    for k in rm_k:
        e_stop_data_template.pop(k)
    return e_stop_data_template


def pack_route_data(dict_like_data):
    routelist_template = {
        "rid": dict_like_data["rid"],
        "rsid": dict_like_data["rsid"],
        # "gid": dict_like_data["gid"],
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
                routestop.rid AS rid,
                routestop.id AS rsid,
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
        cmd = demo_cmd
        raw_data = self._get_list_of_dict(cmd)
        e_stops_dict = {}
        for s in raw_data:
            if s['id'] not in e_stops_dict:
                e_stops_dict.update({s['id']: pack_e_stop_data(s)})
            e_stops_dict[s['id']]['routelist'].append(pack_route_data(s))

        return e_stops_dict

    def get_e_stop_by_ids(self, ids: list):
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
                routestop.rid AS rid,
                routestop.id AS rsid,
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
        cmd = demo_cmd

        raw_data = self._get_list_of_dict(cmd)
        e_stops_dict = {}
        for s in raw_data:
            if s['id'] not in e_stops_dict:
                e_stops_dict.update({s['id']: pack_e_stop_data(s)})
            e_stops_dict[s['id']]['routelist'].append(pack_route_data(s))

        return e_stops_dict

    def get_valid_msgs(self):
        """
            return all messages
        """
        cmd = """
            SELECT 
                * 
            FROM
                estopMsg
            WHERE
                publish = 1 AND expiretime > NOW()
            """
        raw_data = self._get_list_of_dict(cmd)
        return raw_data

    def get_rsid_sid_table(self):
        """
        a list for matching rsid to sid.
        :return:
            list: [
                        {<rsid: int>: <sid: int>},
                        {<rsid: int>: <sid: int>},
                        {<rsid: int>: <sid: int>},
                        ...
                    ]
        """
        cmd = """
                SELECT id as rsid, sid FROM bus.routestop
            """
        raw_data = self._get_list_of_dict(cmd)
        mapping = {}
        for d in raw_data:
            mapping[d['rsid']] = d['sid']
        return mapping
