import pymongo
from config.Configs import Configs
from logs import Logs


def connect():
    try:
        if Configs.BOT_MONGODB_CONNECTION_URL:
            client = pymongo.MongoClient(Configs.BOT_MONGODB_CONNECTION_URL)
            database = client[Configs.BOT_DATABASE_NAME]
            if database:
                return database
            else:
                Logs.log("Database Connection failed.")
                return None
        else:
            Logs.log("Database Client Connection failed.")
            return None
    except Exception as e:
        Logs.log("Database Error : {}".format(e))
        return None
