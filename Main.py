# -*- coding: utf-8 -*-
"""TelegramBot
Original file is located at https://github.com/asirihewage/Athalbota_bot.git
# Telegram Bot
"""

# importing all dependencies
from datetime import datetime
import os
from pyrogram import Client, filters

from models.Group import Group
from utils import Translations, Menus
from utils.Configs import Configs
from utils.Logs import log
from models.Chat import Chat
from models.Message import Message
from models.User import User
from utils.Database import connect

app = Client(Configs.BOT_USERNAME, bot_token=Configs.BOT_TOKEN, parse_mode=Configs.PARSE_MODE)
translation = 0


@app.on_message(filters.text)
async def check_msg(Client, message):
    dateS = message.date
    dateSent = datetime.fromtimestamp(dateS)
    minutes_diff = (datetime.now() - dateSent).total_seconds() / 60.0

    chat_id = None
    if minutes_diff > 3 or message.text.startswith("/") or message.text.startswith("!") or message.chat.type == "bot" \
            or message.from_user.is_restricted or message.from_user.is_scam or message.from_user.is_fake:
        pass

    elif message.chat.type == "private":
        chat_id = message.from_user.id
        if message.from_user.username is None:
            await app.send_message(message.from_user.id, Translations.INCOMPLETE_PROFILE[translation])
        elif User(message, connect()).isGuest():
            await app.send_message(chat_id, Translations.VERIFY_ACCOUNT_LINK[translation].format(Configs.HOSTNAME, chat_id ))
        elif User(message, connect()).isUser():
            Message(message, connect()).toJSON().save()
        elif User(message, connect()).isAdmin():
            Message(message, connect()).toJSON().save()
        else:
            User(message, connect()).toJSON().save()
            Chat(message, connect()).toJSON().save()
            await app.send_message(chat_id, Translations.WELCOME_MESSAGE_GUEST[translation])

    elif message.chat.type == "group":
        chat_id = message.chat.id
        if Group(message, connect()).isGroup():
            Group(message, connect()).toJSON().save()
            await app.send_message(chat_id, Translations.WELCOME_MESSAGE_GROUP[translation])

    else:
        User(message, connect()).toJSON().save().makeGuest()
        await app.send_message(message.from_user.id, Translations.RESTRICTED_USER[translation])


@app.on_callback_query(group=2)
async def callback_query(Client, Query):
    try:
        if User(Query, connect()).isGuest():
            if Query.data == "!help":
                await Query.message.edit(Translations.HELP_TEXT_GUEST[translation])

        if User(Query, connect()).isUser():
            if Query.data == "!help":
                await Query.message.edit(Translations.HELP_TEXT_USER[translation])

        if User(Query, connect()).isAdmin():
            if Query.data == "!help":
                await Query.message.edit(Translations.HELP_TEXT_ADMIN[translation])

            elif Query.data == "!allusers":
                await Query.message.edit(f'😲 All Users:', reply_markup=Menus.get_keyboard('', connect()))

            elif Query.data == "!alladmins":
                await Query.message.edit(f'😎 All Admins:', reply_markup=Menus.get_keyboard('', connect()))

            elif Query.data == "!allgroups":
                await Query.message.edit(f'👤👤👤 All Groups:', reply_markup=Menus.get_keyboard('', connect()))

            elif Query.data == "!addNewAdmin":
                await Query.message.edit(
                    f'✎ Please add new admin like this: <b> admin username </b> \nExample: '
                    f'admin john.')

            elif Query.data.startswith("!verify "):
                user_id = Query.data.replace("!verify ", "")
                if User(Query, connect()).verify(user_id):
                    await Query.message.edit(
                        f"✌ User has been verified")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to verify the user")

            elif Query.data.startswith("!removeUser "):
                user_id = Query.data.replace("!removeUser ", "")
                if User(Query, connect()).removeUser(user_id):
                    await Query.message.edit(
                        f"✌ User @{user_id} has been removed")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to add @{user_id} as an admin.")

            elif Query.data.startswith("!makeAdmin "):
                user_id = Query.data.replace("!makeAdmin ", "")
                if User(Query, connect()).promoteAdmin(user_id):
                    await Query.message.edit(
                        f"✌ User {user_id} has given an admin role.")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to add {user_id} as an admin.")

            elif Query.data.startswith("!remove "):
                user_id = Query.data.replace("!remove ", "")
                if User(Query, connect()).removeAdmin(user_id):
                    await Query.message.edit(
                        f"✌ User @{user_id} removed from admin role.")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to remove {user_id} from admin role.")

            elif Query.data.startswith("!leaveGroup "):
                group_id = Query.data.replace("!leaveGroup ", "")
                if Group(Query, connect()).leave(group_id):
                    await app.leave_chat(int(group_id))
                    await Query.message.edit(
                        f"✌ Bot left from the group!")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, Bot can not leave the group.")

        else:
            if User(Query, connect()).toJSON().save():
                User(Query, connect()).makeGuest()
                await app.send_message(Query.from_user.id, Translations.WELCOME_MESSAGE_GUEST[translation])

    except Exception as e:
        log(e)
        await app.send_message('1664758714', 'Error: {}'.format(str(e)))
        pass


@app.on_message(filters.private & filters.command(['menu'], ['/']), group=2)
async def menu(Client, message):
    if User(message, connect()).isGuest():
        await app.send_message(message.from_user.id, f'Please activate your account.')
    elif User(message, connect()).isUser():
        await message.message.edit(f'😲 User Menu:', reply_markup=Menus.get_keyboard('userMenu', connect()))
    elif User(message, connect()).isAdmin():
        await message.message.edit(f'😲 Admin Menu:', reply_markup=Menus.get_keyboard('adminMenu', connect()))
    else:
        if User(message, connect()).toJSON().save():
            User(message, connect()).makeGuest()
            await app.send_message(message.from_user.id, Translations.WELCOME_MESSAGE_GUEST[translation])


@app.on_message(filters.private & filters.command(['start'], ['/']), group=2)
async def start(Client, message):
    if User(message, connect()).isGuest():
        await app.send_message(message.from_user.id, Translations.VERIFY_ACCOUNT_LINK[translation].format(Configs.HOSTNAME, message.from_user.id))
    elif User(message, connect()).isUser():
        await app.send_message(message.from_user.id, Translations.HELP_TEXT_USER[translation])
    elif User(message, connect()).isAdmin():
        await app.send_message(message.from_user.id, Translations.HELP_TEXT_ADMIN[translation])
    else:
        if User(message, connect()).toJSON().save():
            User(message, connect()).makeGuest()
            await app.send_message(message.from_user.id, Translations.WELCOME_MESSAGE_GUEST[translation])
            await app.send_message(message.from_user.id, Translations.VERIFY_ACCOUNT_LINK[translation].format(Configs.HOSTNAME, message.from_user.id))


@app.on_message(filters.private & filters.command(['help'], ['/']), group=2)
async def helpTopics(Client, message):
    if User(message, connect()).isGuest():
        await app.send_message(message.from_user.id, Translations.HELP_TEXT_GUEST[translation])
    elif User(message, connect()).isUser():
        await app.send_message(message.from_user.id, Translations.HELP_TEXT_USER[translation])
    elif User(message, connect()).isAdmin():
        await app.send_message(message.from_user.id, Translations.HELP_TEXT_ADMIN[translation])
    else:
        if User(message, connect()).toJSON().save():
            User(message, connect()).makeGuest()
            await app.send_message(message.from_user.id, Translations.WELCOME_MESSAGE_GUEST[translation])


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
        if User(message, connect()).toJSON().save():
            User(message, connect()).makeGuest()


log("Poling started...")
app.run()
