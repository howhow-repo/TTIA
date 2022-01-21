import logging

import pymysql

logger = logging.getLogger(__name__)


def is_config_items(configs: dict):
    mandatory_items = ['host', 'port', 'user', 'password', 'db']
    for k in configs.keys():
        if k not in mandatory_items:
            return False
    return True


class MySqlHandler:

    def __init__(self, mysql_configs: dict):
        assert is_config_items(mysql_configs), "There are some config data is missing. " \
                                               "Need 'host', 'port', 'user', 'password', 'db'"
        self.__mysql_configs = mysql_configs
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pymysql.connect(**self.__mysql_configs)
            self.cursor = self.conn.cursor()
            logger.debug("center DB connected: please remember disconnect after used")
        except Exception as err:
            self.disconnect()
            raise ConnectionError(f"ebus center mysql connection error.\n {err}")

    def disconnect(self):
        if isinstance(self.cursor, pymysql.cursors.Cursor):
            self.cursor.close()
            self.cursor = None
        if isinstance(self.conn, pymysql.Connect):
            self.conn.close()
            self.conn = None
        logger.debug("close center DB connection")

    def test_connection(self):
        try:
            self.cursor.execute('SELECT VERSION()')
            data = self.cursor.fetchone()
            print("Database version : %s " % data)
        except Exception as err:
            self.disconnect()
            raise ConnectionError("ebus center mysql test connection fail.")

    def __query(self, sqlcmd) -> pymysql.cursors.Cursor:
        try:
            self.cursor.execute(sqlcmd)
        except pymysql.OperationalError:
            self.connect()
            self.cursor.execute(sqlcmd)
        return self.cursor

    def get_table(self, sqlcmd):
        r = self.__query(sqlcmd)
        return r.fetchall()

    def get_single_data(self, sqlcmd):
        r = self.__query(sqlcmd)
        row = r.fetchone()
        if row is not None:
            return row[0]
        return None
