import logging
import pymongo
from pymongo import MongoClient

logger = logging.getLogger(__name__)


def check_config_items(configs: dict):
    mandatory_items = ['host', 'port', 'user', 'password', 'db']
    for item in mandatory_items:
        if item not in configs.keys():
            raise ValueError(f"Missing key in config: {item}")
    return


class MongoDB:
    """
        Base features for using mongo db.
        Including connect/disconnect; get one or more data; using pure mongo cmd.
    """
    def __init__(self, mongo_config: dict):
        check_config_items(mongo_config)
        self.__ebusMongoDBPath = "mongodb://" + \
                                 mongo_config['user'] + ":" + \
                                 mongo_config['password'] + "@" + \
                                 mongo_config['host'] + ":" + \
                                 str(mongo_config['port']) + "/" + \
                                 mongo_config['db']
        self.db_name = mongo_config['db']
        self.db = None
        self._conn = None

        self.connect()
        self.test_connection()
        self.disconnect()

    def connect(self):
        try:
            self._conn = MongoClient(self.__ebusMongoDBPath, serverSelectionTimeoutMS=5000)
            self.db = self._conn[self.db_name]
            logger.debug("drive DB connected: please remember disconnect after used")
        except Exception as err:
            logger.error(f"something went wrong.\n {err}")
            raise err

    def disconnect(self):
        if isinstance(self._conn, pymongo.MongoClient):
            self._conn.close()
            self._conn = None
        logger.debug("close drive DB connection")

    def test_connection(self):
        try:
            info = self._conn.server_info()
            logger.info({"version": info['version']})
        except Exception as err:
            logger.error("Mongo DB connection test fail")
            raise err

    def list_collections(self):
        try:
            return self.db.list_collection_names()
        except Exception as err:
            logger.error("something went wrong")
            raise err
