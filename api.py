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
from utils.Configs import Configs
from utils.Logs import log

api = Flask(__name__)


# connect to the database
def connect():
    try:
        if Configs.BOT_MONGODB_CONNECTION_URL:
            log("Database Client initialized.")
            client = pymongo.MongoClient(Configs.BOT_MONGODB_CONNECTION_URL)
            database = client[Configs.BOT_DATABASE_NAME]
            if database:
                log("Database Connected.")
                return database
            else:
                log("Database Connection failed.")
                return None
        else:
            log("Database Client Connection failed.")
            return None
    except Exception as e:
        log("Database Error : {}".format(e))
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
            log("Database connection error")
            return False
    except Exception as er:
        print(er)
        return False


@api.route("/")
def index():
    html = '<HTMl><head><meta http-equiv="refresh" content="1; URL={}"></head>Oopz! The link is invalid</HTML>'.format(
        Configs.BOT_LINK)
    return html


@api.route("/verifyuser/<user_id>")
def verifyuser(user_id):
    html = '<HTMl><head><meta http-equiv="refresh" content="2; URL={}"></head>Account Verified!</HTML>'.format(Configs.BOT_LINK)
    if user_id and promote_user(int(user_id)):
        return html
    else:
        return '<HTMl><head><meta http-equiv="refresh" content="2; URL={}"></head>Something went wrong</HTML>'.format(
            Configs.BOT_LINK)
