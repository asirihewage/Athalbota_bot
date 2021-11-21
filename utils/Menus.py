from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models.Chat import Chat
from models.Group import Group
from models.Message import Message
from models.User import User
from utils.Configs import Configs
from utils.Logs import log

adminMenu = InlineKeyboardMarkup(
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

userMenu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=f"♢ සිංහල", callback_data=f"!setTranslate 0"),
            InlineKeyboardButton(text=f"♢ தமிழ்", callback_data=f"!setTranslate 1"),
            InlineKeyboardButton(text=f"♢ English", callback_data=f"!setTranslate 2")
        ]
    ]
)

guestMenu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=f"♢ සිංහල", callback_data=f"!setTranslate 0"),
            InlineKeyboardButton(text=f"♢ தமிழ்", callback_data=f"!setTranslate 1"),
            InlineKeyboardButton(text=f"♢ English", callback_data=f"!setTranslate 2")
        ]
    ]
)

helpMenu = InlineKeyboardMarkup(
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

aboutMenu = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text=f"💢 About Bot", callback_data=f"!aboutBot")
        ],
        [
            InlineKeyboardButton(text=f"💢 About Developer", callback_data=f"!aboutDeveloper")
        ],
        [
            InlineKeyboardButton(text=f"💢 Support", callback_data=f"!support")
        ],
        [
            InlineKeyboardButton(text=f"💢 Feedback", callback_data=f"!feedback")
        ]
    ]
)


def showAllGroups(message, dbCon):
    rows = []
    try:
        groups = Group(message, dbCon).getAllGroups()
        if groups:
            for group in groups:
                row = [
                    InlineKeyboardButton(text=f"{group['group_id']}", callback_data=f"!"),
                    InlineKeyboardButton(text=f"𝗟𝗲𝗮𝘃𝗲 𝗚𝗿𝗼𝘂𝗽",
                                         callback_data=f"!leaveGroup {group['group_id']}")
                ]
                rows.append(row)
            return InlineKeyboardMarkup(rows)
        else:
            return None
    except Exception as er:
        log(er)
        return None


def showAllUsers(message, dbCon):
    rows = []
    try:
        users = User(message, dbCon).getAllUsers()
        if users:
            for user in users:
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
            return None
    except Exception as er:
        log(er)
        return None


def showAllAdmins(message, dbCon):
    rows = []
    try:
        admins = User(message, dbCon).getAllUsers()
        if admins:
            for user in admins:
                row = [
                    InlineKeyboardButton(text=f"{user['username']}", callback_data=f"!profile {user['username']}"),
                    InlineKeyboardButton(text=f"𝗥𝗲𝗺𝗼𝘃𝗲", callback_data=f"!remove {user['username']}")
                ]
                rows.append(row)
            return InlineKeyboardMarkup(rows)
        else:
            return None
    except Exception as er:
        log(er)
        return None


def showAllGuests(message, dbCon):
    rows = []
    try:
        guests = User(message, dbCon).getAllGuests()
        if guests:
            for guest in guests:
                row = [
                    InlineKeyboardButton(text=f"{guest['username']}", callback_data=f"!"),
                    InlineKeyboardButton(text=f"🆅🅴🆁🅸🅵🆈",
                                         callback_data=f"!verify {guest['id']}")
                ]
                rows.append(row)
            return InlineKeyboardMarkup(rows)
        else:
            log("Database connection error")
            return None
    except Exception as er:
        log(er)
        return None


def get_keyboard(menu, dbCon):
    if menu is 'adminMenu':
        return adminMenu
    elif menu is 'userMenu':
        return userMenu
    elif menu is 'guestMenu':
        return guestMenu
    elif menu is 'helpMenu':
        return helpMenu
    elif menu is 'aboutMenu':
        return aboutMenu
    elif menu is 'showAllAdmins':
        return showAllAdmins(menu, dbCon)
    elif menu is 'showAllGroups':
        return showAllGroups(menu, dbCon)
    elif menu is 'showAllUsers':
        return showAllUsers(menu, dbCon)
    elif menu is 'showAllGuests':
        return showAllGuests(menu, dbCon)
