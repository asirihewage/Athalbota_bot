# -*- coding: utf-8 -*-
"""TelegramBot
Original file is located at https://github.com/asirihewage/Athalbota_bot.git
# Telegram Bot
"""

# importing all dependencies
import os
from pyrogram import Client, filters
from config.Configs import Configs
from logs import Logs
from models.Chat import Chat
from models.Message import Message
from models.User import User
from models.Database import connect

app = Client(Configs.BOT_USERNAME, bot_token=Configs.BOT_TOKEN, parse_mode=Configs.PARSE_MODE)


@app.on_message(filters.text)
async def check_msg(Client, message):
    Message(message, connect()).toJSON().save()
    User(message, connect()).toJSON().save()
    Chat(message, connect()).toJSON().save()
    await app.send_message(message.from_user.id, f'Unauthorised. /help')


@app.on_callback_query(group=2)
async def callback_query(Client, Query):
    await app.send_message(Query.from_user.id, f'Unauthorised. /help')


@app.on_message(filters.private & filters.command(['errors'], ['/']), group=2)
async def errors(Client, message):
    if User(message, connect()).isAdmin():
        err = ""
        thisFolder = os.path.dirname(os.path.abspath(__file__))
        errorLog = os.path.join(thisFolder, 'logs/logger.log')
        with open(errorLog) as file:
            for line in (file.readlines()[-10:]):
                err = err + line
        await app.send_message(message.from_user.id, f'ERRORS: <pre> {err} </pre>')
    else:
        User(message, connect()).save().makeGuest()
        await app.send_message(message.from_user.id, f'Unauthorised. /help')


Logs.log("Poling started...")
app.run()
