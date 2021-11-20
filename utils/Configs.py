import configparser
import os


class Configs:
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    initfile = os.path.join(thisfolder, '../config/configs.init')
    configParser = configparser.RawConfigParser()
    configParser.read(initfile)

    BOT_MONGODB_CONNECTION_URL = configParser.get('dbconfig', 'connection_url')
    BOT_DATABASE_NAME = configParser.get('dbconfig', 'database_name')
    BOT_TOKEN = configParser.get('botconfig', 'token')
    ANSWER_ACCURACY_PERCENTAGE = configParser.get('botconfig', 'accuracy')
    HOSTNAME = configParser.get('serverconfig', 'host_name')
    BOT_USERNAME = configParser.get('botconfig', 'username')
    PARSE_MODE = configParser.get('botconfig', 'parse_mode')
