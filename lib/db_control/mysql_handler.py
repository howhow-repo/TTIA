import logging
import pymysql

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s',)
logger = logging.getLogger(__name__)


def check_config_items(configs: dict):
    mandatory_items = ['host', 'port', 'user', 'password', 'db']
    for item in mandatory_items:
        if item not in configs.keys():
            raise ValueError(f"Missing key in config: {item}")
    return


def dictfetchall(cursor):
    """Returns all rows from a cursor as a list of dicts"""
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # list of dict


class MySqlHandler:
    """
        Base features for using mysql.
        Including connect/disconnect; get one or more data; using pure sql cmd.
    """
    def __init__(self, mysql_config: dict):
        check_config_items(mysql_config)

        self.__mysql_config = mysql_config
        self.conn = None
        self.cursor = None

        self.connect()
        self.test_connection()
        self.disconnect()

    def connect(self):
        try:
            self.conn = pymysql.connect(**self.__mysql_config)
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

    def __query(self, sqlcmd) -> pymysql.cursors.Cursor:
        if self.cursor is None:
            raise ConnectionError("DB is not connected yet. Please try method 'connect().")
        try:
            self.cursor.execute(sqlcmd)
        except pymysql.OperationalError:
            logger.warning("Connection fail, reconnecting...")
            self.connect()
            self.cursor.execute(sqlcmd)
        return self.cursor

    def test_connection(self):
        try:
            ver = self.get_single_data('SELECT VERSION()')
            logger.info(f"Test Connecting success; MySQL version : {ver} ")
        except Exception as err:
            self.disconnect()
            raise ConnectionError(f"ebus center mysql test connection fail.\n {err}")

    def _get_list_of_dict(self, sqlcmd):
        r = self.__query(sqlcmd)
        return dictfetchall(r)

    def get_single_data(self, sqlcmd):
        r = self.__query(sqlcmd)
        row = r.fetchone()
        if row is not None:
            return row[0]
        return None
