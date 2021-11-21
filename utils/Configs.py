import configparser
import os


class Configs:
    # thisfolder = os.path.dirname(os.path.abspath(__file__))
    # initfile = os.path.join(thisfolder, '../config/configs.init')
    # configParser = configparser.RawConfigParser()
    # configParser.read(initfile)
    #
    # BOT_MONGODB_CONNECTION_URL = configParser.get('dbconfig', 'connection_url')
    # BOT_DATABASE_NAME = configParser.get('dbconfig', 'database_name')
    # BOT_TOKEN = configParser.get('botconfig', 'token')
    # ANSWER_ACCURACY_PERCENTAGE = configParser.get('botconfig', 'accuracy')
    # HOSTNAME = configParser.get('serverconfig', 'host_name')
    # BOT_USERNAME = configParser.get('botconfig', 'username')
    # PARSE_MODE = configParser.get('botconfig', 'parse_mode')
    # API_HOST = configParser.get('serverconfig', 'api_host')
    # BOT_LINK = configParser.get('botconfig', 'bot_link')

    BOT_MONGODB_CONNECTION_URL = os.environ.get('BOT_MONGODB_CONNECTION_URL', 3)
    BOT_DATABASE_NAME = os.environ.get('BOT_DATABASE_NAME', 3)
    BOT_TOKEN = os.environ.get('BOT_TOKEN', 3)
    ANSWER_ACCURACY_PERCENTAGE = os.environ.get('ANSWER_ACCURACY_PERCENTAGE', 3)
    HOSTNAME = os.environ.get('HOSTNAME', 3)
    BOT_USERNAME = os.environ.get('BOT_USERNAME', 3)
    PARSE_MODE = os.environ.get('PARSE_MODE', 3)
    API_HOST = os.environ.get('API_HOST', 3)
    BOT_LINK = os.environ.get('BOT_LINK', 3)
