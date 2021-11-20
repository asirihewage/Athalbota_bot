# -*- coding: utf-8 -*-
"""TelegramBot
Original file is located at hhttps://github.com/asirihewage/Friendly_CryptoBot
# Telegram Bot
"""

# importing all dependencies
import logging
import logging.handlers as handlers
import pymongo
from flask import Flask

api = Flask(__name__)

# Getting environment variables from Heroku configs if not overriden
BOT_MONGODB_CONECTION_URL = "mongodb+srv://sampleUsername:samplePassword@cluster0.lok9v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
BOT_DATABASE_NAME = "TelegramBotFriendly_CryptoBot"
ANSWER_ACCURACY_PERCENTAGE = 75
HOSTNAME = "https://friendlycryptobot.herokuapp.com/"
BOT_LINK = "https://t.me/Friendly_CryptoBot"

# Initialize logging for debugging purpose
formatter = logging.Formatter(
    '%(asctime)s * %(name)s * %(levelname)s * [%(filename)s:%(lineno)s  %(funcName)20s() ] %(message)s')
logger = logging.getLogger()
logHandler = handlers.TimedRotatingFileHandler('logs/logger.log', when='M', interval=53, backupCount=24)
logHandler.setLevel(logging.ERROR)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.error("Bot initialized")


# connect to the database
def connect():
    try:
        if BOT_MONGODB_CONECTION_URL:
            logger.error("Database Client initialized.")
            client = pymongo.MongoClient(BOT_MONGODB_CONECTION_URL)
            database = client[BOT_DATABASE_NAME]
            if database:
                logger.error("Database Connected.")
                return database
            else:
                logger.error("Database Connection failed.")
                return None
        else:
            logger.error("Database Client Connection failed.")
            return None
    except Exception as e:
        logger.error("Database Error : {}".format(e))
        return None


dbConnection = connect()


def promote_user(user_id):
    try:
        if user_id and dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": int(user_id)}):
                usersCollection.update_one({"id": int(user_id)}, {"$set": {"level": 1}})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        print(er)
        return False


@api.route("/")
def index():
    html = '<HTMl><head><meta http-equiv="refresh" content="1; URL={}"></head>Oopz! The link is invalid</HTML>'.format(BOT_LINK)
    return html


@api.route("/verifyuser/<user_id>")
def verifyuser(user_id):
    html = '<HTMl><head><meta http-equiv="refresh" content="2; URL={}"></head>Account Verified!</HTML>'.format(BOT_LINK)
    if user_id and promote_user(int(user_id)):
        return html
    else:
        return '<HTMl><head><meta http-equiv="refresh" content="2; URL={}"></head>Something went wrong</HTML>'.format(BOT_LINK)

