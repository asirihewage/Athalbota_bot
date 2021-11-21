from utils.Configs import Configs
from utils.Logs import log


class Message:

    def __init__(self, message, dbCon):
        self.message_id = message.message_id
        self.from_user_id = message.from_user.id
        self.date = message.date
        self.chat_id = message.chat.id
        self.text = message.text
        self.type = message.chat.type
        self.database = dbCon
        self.jsonObj = None
        self.message = message

    def toJSON(self):
        self.jsonObj = {
            "chat_id": self.chat_id,
            "message_id": self.message_id,
            "date": self.date,
            "type": self.type,
            "text": self.text,
            "user": self.from_user_id,
        }
        return self

    def isTextMessage(self):
        if self.message.entities and len(self.message.entities) > 0:
            return False
        else:
            return True

    def save(self):
        try:
            if self.database and self.isTextMessage():
                messagesCollection = self.database.get_collection("messages")
                if messagesCollection.find_one({"message_id": self.message_id, "chat_id": self.chat_id}):
                    messagesCollection.update_one({"message_id": self.message_id, "chat_id": self.chat_id}, {"$set": self.jsonObj})
                    return self
                else:
                    messagesCollection.insert_one(self.jsonObj)
                    return self
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def getAllUsers(self):
        try:
            if self.database:
                messagesCollection = self.database.get_collection("messages")
                if messagesCollection.count_documents({}) and messagesCollection.count_documents({}) > 0:
                    return messagesCollection.find({})
                elif messagesCollection.count_documents({}) and messagesCollection.count_documents({}) <= 0:
                    log("No chats")
                    return None
                else:
                    log("Something went wrong when fetching groups")
            else:
                log("Database connection error")
                return None
        except Exception as e:
            log(e)
            return None
