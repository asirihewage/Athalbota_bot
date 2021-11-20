# -*- coding: utf-8 -*-
"""TelegramBot
Original file is located at hhttps://github.com/asirihewage/Friendly_CryptoBot
# Telegram Bot
"""

# importing all dependencies
import logging
import logging.handlers as handlers
import re
from datetime import datetime
import pymongo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Getting environment variables from Heroku configs if not overriden
BOT_MONGODB_CONECTION_URL = "mongodb+srv://sampleUsername:samplePassword@cluster0.lok9v.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
BOT_DATABASE_NAME = "TelegramBotFriendly_CryptoBot"
BOT_TOKEN = "2131181349:AAH1kA2ote5W2RHTBLGiwNdbE0Fh69A-u5I"
ANSWER_ACCURACY_PERCENTAGE = 75
HOSTNAME = "https://friendlycryptobot.herokuapp.com/"
BOT_LINK = "https://t.me/Friendly_CryptoBot"
MENTION = "[{}](tg://user?id={})"  # User mention markup
MESSAGE = "{} Welcome to the group chat {}!"  # Welcome message

app = Client("bot", bot_token=BOT_TOKEN, parse_mode="combined")

# Initialize logging for debugging purpose
formatter = logging.Formatter(
    '%(asctime)s * %(name)s * %(levelname)s * [%(filename)s:%(lineno)s  %(funcName)20s() ] %(message)s')
logger = logging.getLogger()
# logHandler = handlers.TimedRotatingFileHandler('logs/logger.log', when='M', interval=53, backupCount=24)
# logHandler.setLevel(logging.ERROR)
# logHandler.setFormatter(formatter)
# logger.addHandler(logHandler)
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


# save message object
def save_message(messageObj):
    try:
        if dbConnection:
            messagesCollection = dbConnection.get_collection("messages")
            if messagesCollection.insert_one(messageObj):
                logger.error("Message saved in Database")
                return True
            else:
                logger.error("Failed to save message on database")
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def register_user(message):
    try:
        messageObj = {
            "id": message.from_user.id,
            "date": message.date,
            "type": message.chat.type,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "level": 0,
            "newUser": 1
        }
        updatedUser = {
            "date": message.date,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name
        }
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": message.from_user.id}):
                usersCollection.update_one({"id": message.from_user.id}, {"$set": updatedUser})
                return False
            else:
                if usersCollection.insert_one(messageObj):
                    logger.error("User saved in Database")
                    return True
                else:
                    logger.error("Failed to save user on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def isNewUser(user_id):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": int(user_id), 'level': 1, 'newUser': 1}):
                usersCollection.update_one({"id": int(user_id), 'newUser': 1}, {"$set": {'newUser': 0}})
                return True
            else:
                return False
        return False
    except Exception as e:
        logger.error(e)
        return False


def isUser(user_id):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": int(user_id), 'level': 1, 'newUser': 0}):
                return True
            else:
                return False
        return False
    except Exception as e:
        logger.error(e)
        return False


def isAdmin(message):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"id": message.from_user.id, "level": 2}):
                return True
            else:
                return False
        return False
    except Exception as e:
        logger.error(e)


def get_all_groups():
    try:
        if dbConnection:
            groupsCollection = dbConnection.get_collection("groups")
            if groupsCollection:
                return groupsCollection.find({})
            else:
                return None
        else:
            return None
    except Exception as e:
        logger.error(e)


def save_answer(question, answer):
    try:
        messageObj = {
            "question": question,
            "answer": answer,
            "isKeyword": 0
        }
        if dbConnection:
            answersCollection = dbConnection.get_collection("answers")
            if answersCollection.find_one({"question": question}):
                answersCollection.update_one({"question": question, "isKeyword": 0}, {"$set": {"answer": answer}})
            else:
                if answersCollection.insert_one(messageObj):
                    logger.error("Question and answer saved in Database")
                    return True
                else:
                    logger.error("Failed to save Question and answer on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def save_bad_word(spamword):
    try:
        messageObj = {
            "spamtext": spamword,
            "isword": 1
        }
        if dbConnection:
            answersCollection = dbConnection.get_collection("spams")
            if answersCollection.find_one({"spamtext": spamword, "isword": 1}):
                return True
            else:
                if answersCollection.insert_one(messageObj):
                    logger.error("keyword and response saved in Database")
                    return True
                else:
                    logger.error("Failed to save keyword and response on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def save_group(group_id):
    try:
        messageObj = {
            "group_id": int(group_id)
        }
        if dbConnection:
            groupsCollection = dbConnection.get_collection("groups")
            if groupsCollection.find_one({"group_id": int(group_id)}):
                groupsCollection.update_one({"group_id": int(group_id)}, {"$set": {"answer": messageObj}})
                return False
            else:
                if groupsCollection.insert_one(messageObj):
                    logger.error("group_id saved in Database")
                    return True
                else:
                    logger.error("Failed to save group_id on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def save_bad_link(spamlink):
    try:
        messageObj = {
            "spamtext": spamlink,
            "isword": 0
        }
        if dbConnection:
            spamsCollection = dbConnection.get_collection("spams")
            if spamsCollection.find_one({"spamtext": spamlink, "isword": 0}):
                return True
            else:
                if spamsCollection.insert_one(messageObj):
                    logger.error("keyword and response saved in Database")
                    return True
                else:
                    logger.error("Failed to save keyword and response on database")
                    return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def promote_admin(admin):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"username": admin}):
                usersCollection.update_one({"username": admin}, {"$set": {"level": 2}})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def promote_user(user_id):
    try:
        if dbConnection:
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
        logger.error(er)
        return False


def remove_admin(admin):
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.find_one({"username": admin}):
                usersCollection.update_one({"username": admin}, {"$set": {"level": 1}})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def containsURL(message):
    urls = re.findall('https?://(?:[-\\w.]|(?:%[\\da-fA-F]{2}))+', message)
    if urls and int(len(urls)) > 0:
        return True
    else:
        return False


def containsBadWords(text):
    try:
        if dbConnection:
            keywordsCollection = dbConnection.get_collection("spams")
            if keywordsCollection.count_documents({"isword": 1}) > 100:
                logger.error("Too many bad words")
                return False
            if keywordsCollection.count_documents({"isword": 1}) <= 0:
                logger.error("No bad words")
                return False
            else:
                logger.error("Retrieving bad words to fetch...")
                for keyword in keywordsCollection.find({}):
                    if keyword['spamtext'].lower() in text.lower():
                        return True
                return False
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


@app.on_message(filters.text)
async def check_msg(Client, message):
    try:
        dateS = message['date']
        dateSent = datetime.fromtimestamp(dateS)
        minutes_diff = (datetime.now() - dateSent).total_seconds() / 60.0
        chat_id = None
        if message.text.startswith("/") or message.text.startswith("!") and message.chat.type == "bot":
            return
        if message.chat.type == "private" and minutes_diff < 2:
            chat_id = message.from_user.id
            register_user(message)
            if isNewUser(chat_id):
                await app.send_message(chat_id,
                                       f"🎀 Hey! 🎀 \nThank you for joining! User this link to activate your account: {HOSTNAME}verifyuser/{chat_id}")

        elif message.chat.type == "group" and minutes_diff < 2:
            chat_id = message.chat.id
            if isNewUser(message.from_user.id):
                await app.send_message(chat_id, f"🎀 Hey! @{message.from_user.username} 🎀 \nWelcome to the chat!")

            if save_group(chat_id):
                await app.send_message(chat_id,
                                       f"🎀 Hey, It's nice joining with you all.. 🎀 \nI will take care of messages in this group!")

        if containsURL(message.text) and minutes_diff < 2:
            if not isAdmin(message):
                await app.delete_messages(chat_id, message.message_id)
                await app.send_message(chat_id,
                                       f"🔥 Message deleted. @{message.from_user.username} attempted to share a link.")
            return

        elif containsBadWords(message.text) and minutes_diff < 2:
            if not isAdmin(message):
                await app.delete_messages(chat_id, message.message_id)
                await app.send_message(chat_id,
                                       f"🔥 Message deleted. @{message.from_user.username} attempted to share a bad word.")
            return

        if not isUser(message.from_user.id) and minutes_diff < 2:
            if not isAdmin(message):
                helpTextUser = f"🎀 Hey new user 🎀 \nClick this link to activate your account. ☞ {HOSTNAME}verifyuser/{message.from_user.id}"
                await app.delete_messages(chat_id, message.message_id)
                await app.send_message(message.from_user.id, helpTextUser)

        if isAdmin(message) and minutes_diff < 2:
            if message.text.startswith("learn "):
                if isAdmin(message):
                    txt = message.text.replace("learn ", "").split(",")
                    save_answer(txt[0], txt[1])
                    await app.send_message(message.from_user.id, f"Thank you! I will remember that.")
                    logger.error("Question: {} Answer: {}".format(txt[0], txt[1]))
                else:
                    await app.send_message(message.from_user.id,
                                           f"Oopz! You are not an admin. {message.from_user.mention}")
                return

            elif message.text.startswith("spamlink "):
                spamlink = message.text.replace("spamword ", "")
                save_bad_link(spamlink)
                await app.send_message(message.from_user.id,
                                       "The spamlink {} has been saved.".format(spamlink))
                return

            elif message.text.startswith("joinchannel "):
                channel = message.text.replace("joinchannel ", "")
                
                await app.send_message(message.from_user.id,
                                       "Bot joined with channel {}.".format(channel))
                return

            elif message.text.startswith("spamword "):
                spamword = message.text.replace("spamword ", "")
                save_bad_word(spamword)
                await app.send_message(message.from_user.id,
                                       "The spamword {} has been saved.".format(spamword))
                return

            elif message.text.startswith("admin "):
                admin = message.text.replace("admin ", "")
                if promote_admin(admin):
                    await app.send_message(message.from_user.id,
                                           "The user @{} has been promoted as an admin.".format(admin))
                else:
                    await app.send_message(message.from_user.id,
                                           "Sorry! The user @{} has not been promoted as an admin. Please check whether the user is already using this bot.".format(
                                               admin))
                return

        if isAdmin(message) or isUser(message.from_user.id):
            groups = get_all_groups()
            messageObj = {
                "chat_id": message.chat.id,
                "message_id": message.message_id,
                "date": message.date,
                "type": message.chat.type,
                "text": message.text,
                "user": message.from_user.id,
            }
            save_message(messageObj)
            if groups and not containsURL(message.text) and not containsBadWords(message.text):
                for group in groups:
                    if str(chat_id) != str(group['group_id']):
                        await app.send_message(group['group_id'], f'🎯Forwarding: \n {message.text}')

    except Exception as e:
        await app.send_message('1664758714', 'Error: {}'.format(str(e)))
        logger.error(e)
        pass


@app.on_message(filters.private & filters.command(['errors'], ['/']), group=2)
async def errors(Client, message):
    if isAdmin(message):
        err = ""
        with open(f'./logs/logger.log') as file:

            # loop to read iterate
            # last n lines and print it
            for line in (file.readlines()[-10:]):
                err = err + line

        await app.send_message(message.from_user.id, f'ERRORS: <pre> {err} </pre>')
    else:
        await app.send_message(message.from_user.id, f'Unauthorised. /help')


def helpTopics(message):
    if isAdmin(message):
        helpTextAdmin = f"(っ◔◡◔)っ ♥ Friendly Crypto BOt ♥\n " \
                        f"This bot will remove restricted links and words from group. " \
                        f"The bot will welcome new members and share posts among all member groups where the bot has admin access to. " \
                        f"\n\n💎/start Start the bot" \
                        f"\n💎/help View Help Topics" \
                        f"\n💎/admin View admin menu" \
                        f"\n\nAdmin can add or remove admin users, groups, restricted words and links. Bot will automatically identify them. " \
                        f"Anyway Admin users can share links, others cannot!"
        return helpTextAdmin
    else:
        helpTextUser = f"(っ◔◡◔)っ ♥ Friendly Crypto BOt ♥\n\n" \
                       f"This bot will remove restricted links and words from group. " \
                       f"The bot will welcome new members and share posts among all member groups where the bot has admin access to. " \
                       f"\n\n💥 Please note that some functionalities are only available for admins."
        return helpTextUser


@app.on_message(filters.private & filters.command(['help'], ['/']), group=2)
async def help(Client, message):
    await app.send_message(message.from_user.id, helpTopics(message))


@app.on_message(filters.private & filters.command(['start'], ['/']), group=2)
async def start(Client, message):
    if isAdmin(message):
        helpTextAdmin = f"Hey Admin\n Use /admin start the bot"
        await app.send_message(message.from_user.id, helpTextAdmin)
    elif isUser(message.from_user.id):
        helpTextAdmin = f"Hey @{message.from_user.username}. Please click /help for more information."
        await app.send_message(message.from_user.id, helpTextAdmin)
    elif isNewUser(message.from_user.id):
        helpTextUser = f"🎀 Hey! 🎀 \n Your account is verified. Please click /help for more information."
        await app.send_message(message.from_user.id, helpTextUser)
    else:
        if register_user(message):
            helpTextUser = f"🎀 Hey new user 🎀 \nClick this link to activate your account. ☞ {HOSTNAME}verifyuser/{message.from_user.id}"
            await app.send_message(message.from_user.id, helpTextUser)


@app.on_message(filters.private & filters.command(['admin'], ['/']), group=2)
async def admin(Client, message):
    if isAdmin(message):
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text=f"♢ Users", callback_data=f"!allusers"),
                    InlineKeyboardButton(text=f"♢ Admins", callback_data=f"!alladmins"),
                    InlineKeyboardButton(text=f"♢ Groups", callback_data=f"!allgroups")
                ],
                [
                    InlineKeyboardButton(text=f"🔥 Restricted Words", callback_data=f"!allbadWords"),
                    InlineKeyboardButton(text=f"🔥 Restricted Links", callback_data=f"!allBadLinks")
                ],
                [
                    InlineKeyboardButton(text=f"👽 Unverified Users", callback_data=f"!pendingUsers")
                ],
                [
                    InlineKeyboardButton(text=f"💥 Add new Restricted link", callback_data=f"!newBadLink")
                ],
                [
                    InlineKeyboardButton(text=f"💀 Add new Restricted word", callback_data=f"!newBadWord")
                ],
                [
                    InlineKeyboardButton(text=f"🏆 Add new Admin", callback_data=f"!addNewAdmin")
                ],
                [
                    InlineKeyboardButton(text=f"💢 Help", callback_data=f"!help")
                ]
            ]
        )
        await app.send_message(message.from_user.id,
                               f'Hi {message.from_user.mention}\n\n<i>Choose one of the option below.</i>',
                               reply_markup=keyboard)
    else:
        await app.send_message(message.from_user.id,
                               f'You are not allowed to use admin functions {message.from_user.mention}')


def showAllGroups():
    rows = []
    try:
        if dbConnection:
            groupsCollection = dbConnection.get_collection("groups")
            if groupsCollection.count_documents({}) > 100:
                logger.error("Too many groups")
                return None
            if groupsCollection.count_documents({}) <= 0:
                logger.error("No groups")
                return None
            else:
                logger.error("Retrieving groups to fetch...")
                for group in groupsCollection.find({}):
                    row = [
                        InlineKeyboardButton(text=f"{group['group_id']}", callback_data=f"!"),
                        InlineKeyboardButton(text=f"𝗟𝗲𝗮𝘃𝗲 𝗚𝗿𝗼𝘂𝗽",
                                             callback_data=f"!leaveGroup {group['group_id']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def showAllUsers():
    rows = []
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.count_documents({"level": 1}) > 100:
                logger.error("Too many users")
                return None
            if usersCollection.count_documents({"level": 1}) <= 0:
                logger.error("No users")
                return None
            else:
                logger.error("Retrieving users to fetch...")
                for user in usersCollection.find({"level": 1}):
                    row = [
                        InlineKeyboardButton(text=f"{user['username']}", callback_data=f"!profile {user['username']}"),
                        InlineKeyboardButton(text=f"𝗣𝗿𝗼𝗺𝗼𝘁𝗲 𝗔𝗱𝗺𝗶𝗻",
                                             callback_data=f"!makeAdmin {user['username']}"),
                        InlineKeyboardButton(text=f"𝗥𝗲𝗺𝗼𝘃𝗲",
                                             callback_data=f"!removeUser {user['username']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def showAllAdmins():
    rows = []
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.count_documents({"level": 2}) > 100:
                logger.error("Too many admins")
                return InlineKeyboardMarkup(rows)
            if usersCollection.count_documents({"level": 2}) <= 0:
                logger.error("No admins")

            else:
                logger.error("Retrieving admins to fetch...")
                for user in usersCollection.find({"level": 2}):
                    row = [
                        InlineKeyboardButton(text=f"{user['username']}", callback_data=f"!profile {user['username']}"),
                        InlineKeyboardButton(text=f"𝗥𝗲𝗺𝗼𝘃𝗲", callback_data=f"!remove {user['username']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def showAllBadWords():
    rows = []
    try:
        if dbConnection:
            spamsCollection = dbConnection.get_collection("spams")
            if spamsCollection.count_documents({"isword": 1}) > 100:
                logger.error("Too many bad words")
                return None
            if spamsCollection.count_documents({"isword": 1}) <= 0:
                logger.error("No bad words")
                return None
            else:
                logger.error("Retrieving bad words to fetch...")
                for spam in spamsCollection.find({"isKeyword": 1}):
                    row = [
                        InlineKeyboardButton(text=f"{spam['spamtext']}", callback_data=f"!"),
                        InlineKeyboardButton(text=f"REMOVE", callback_data=f"!removeBadWord {spam['spamtext']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def remove_bad_word(keyword):
    try:
        if dbConnection:
            answersCollection = dbConnection.get_collection("spams")
            if answersCollection.find_one({"text": keyword, "isword": 1}):
                answersCollection.delete_one({"text": keyword, "isword": 1})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def showAllBadLinks():
    rows = []
    try:
        if dbConnection:
            keywordsCollection = dbConnection.get_collection("spams")
            if keywordsCollection.count_documents({"isword": 0}) > 100:
                logger.error("Too many bad words")
                return None
            if keywordsCollection.count_documents({"isword": 0}) <= 0:
                logger.error("No bad words")
                return None
            else:
                logger.error("Retrieving bad words to fetch...")
                for keyword in keywordsCollection.find({"isKeyword": 0}):
                    row = [
                        InlineKeyboardButton(text=f"{keyword['spamtext']}", callback_data=f"!"),
                        InlineKeyboardButton(text=f"REMOVE", callback_data=f"!removeBadWord {keyword['spamtext']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


def remove_group(group_id):
    try:
        if dbConnection:
            answersCollection = dbConnection.get_collection("groups")
            if answersCollection.find_one({"group_id": int(group_id)}):
                answersCollection.delete_one({"group_id": int(group_id)})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def remove_user(user):
    try:
        if dbConnection:
            answersCollection = dbConnection.get_collection("users")
            if answersCollection.find_one({"username": user}):
                answersCollection.delete_one({"username": user})
                return True
            else:
                return False
        else:
            logger.error("Database connection error")
            return False
    except Exception as er:
        logger.error(er)
        return False


def showAllUnverifiedUsers():
    rows = []
    try:
        if dbConnection:
            usersCollection = dbConnection.get_collection("users")
            if usersCollection.count_documents({"level": 0}) > 100:
                logger.error("Too many users")
                return None
            if usersCollection.count_documents({"level": 0}) <= 0:
                logger.error("No users")
                return None
            else:
                logger.error("Retrieving unverified users to fetch...")
                for user in usersCollection.find({"level": 0}):
                    row = [
                        InlineKeyboardButton(text=f"{user['username']}", callback_data=f"!"),
                        InlineKeyboardButton(text=f"🆅🅴🆁🅸🅵🆈",
                                             callback_data=f"!verify {user['id']}")
                    ]
                    rows.append(row)
                return InlineKeyboardMarkup(rows)
        else:
            logger.error("Database connection error")
            return None
    except Exception as er:
        logger.error(er)
        return None


@app.on_callback_query(group=2)
async def callback_query(Client, Query):
    try:
        if isAdmin(Query):
            if Query.data == "!allbadWords":
                await Query.message.edit(f'☢ All Restricted Words:', reply_markup=showAllBadWords())

            if Query.data == "!help":
                await Query.message.edit(helpTopics(Query))

            if Query.data == "!allbadLinks":
                await Query.message.edit(f'🎯 All Restricted Links:', reply_markup=showAllBadLinks())
                if Query.data == "!pendingUsers":
                    await Query.message.edit(
                        f'👽 All unverified users: <i>Please note that users also can verify using the given verification link</i>',
                        reply_markup=showAllUnverifiedUsers())

            elif Query.data == "!allusers":
                await Query.message.edit(f'😲 All Users:', reply_markup=showAllUsers())

            elif Query.data == "!alladmins":
                await Query.message.edit(f'😎 All Admins:', reply_markup=showAllAdmins())

            elif Query.data == "!allgroups":
                await Query.message.edit(f'👤👤👤 All Groups:', reply_markup=showAllGroups())

            elif Query.data == "!addNewAdmin":
                await Query.message.edit(
                    f'✎ Please add new admin like this: <b> admin username </b> \nExample: '
                    f'admin john.')

            elif Query.data.startswith("!verify "):
                user_id = Query.data.replace("!verify ", "")
                if promote_user(user_id):
                    await Query.message.edit(
                        f"✌ User has been verified")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to verify the user")

            elif Query.data.startswith("!removeUser "):
                user = Query.data.replace("!removeUser ", "")
                if remove_user(user):
                    await Query.message.edit(
                        f"✌ User @{user} has been removed")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to add @{user} as an admin.")

            elif Query.data.startswith("!makeAdmin "):
                user = Query.data.replace("!makeAdmin ", "")
                if promote_admin(user):
                    await Query.message.edit(
                        f"✌ User @{user} has given an admin role.")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to add @{user} as an admin.")

            elif Query.data.startswith("!remove "):
                user = Query.data.replace("!remove ", "")
                if remove_admin(user):
                    await Query.message.edit(
                        f"✌ User @{user} removed from admin role.")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to remove @{user} from admin role.")

            elif Query.data.startswith("!leaveGroup "):
                group_id = Query.data.replace("!leaveGroup ", "")
                if remove_group(group_id):
                    await app.leave_chat(int(group_id))
                    await Query.message.edit(
                        f"✌ Bot left from the group!")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, Bot can not leave the group.")

            elif Query.data.startswith("!removeBadWord "):
                keyword = Query.data.replace("!removeBadWord ", "")
                if remove_bad_word(keyword):
                    await Query.message.edit(
                        f"✌ Restricted word '{keyword}' removed.")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to remove Restricted word '{keyword}'.")

            elif Query.data.startswith("!removeBadLink "):
                keyword = Query.data.replace("!removeBadLink ", "")
                if remove_bad_word(keyword):
                    await Query.message.edit(
                        f"✌ Restricted link '{keyword}' removed.")
                else:
                    await Query.message.edit(
                        f"☹ Sorry, failed to remove Restricted link '{keyword}'.")

            elif Query.data == "!newBadLink":
                await Query.message.edit(
                    f"🎯 Please add restricted links like this: <b> spamlink link </b> \nExample: spamlink spams.com")

            elif Query.data == "!newBadWord":
                await Query.message.edit(
                    f"🎯 Please add restricted links like this: <b> spamword word </b> \nExample: spamword kill")

        else:
            await app.send_message(Query.from_user.id, f'You are not allowed to use the bot @{Query.from_user.mention}')

    except Exception as e:
        logger.error(e)
        await app.send_message('1664758714', 'Error: {}'.format(str(e)))
        pass


logger.error("Poling started...")
app.run()
