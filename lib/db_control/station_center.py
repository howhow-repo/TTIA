from .mysql_handler import MySqlHandler


class StationCenter(MySqlHandler):
    def __init__(self, mysql_configs: dict):
        super().__init__(mysql_configs)

    def get_e_stops(self):
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

        return self.get_table(cmd)

    def get_e_stop_router(self):
        condition = ''
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
