from logs import Logs


class Chat:
    def __init__(self, message, dbCon):
        self.chat_id = message.chat.id
        self.type = message.chat.type
        self.is_verified = message
        self.is_restricted = message
        self.is_scam = message
        self.is_fake = message
        self.is_support = message.chat.is_support
        self.from_user_id = message.from_user.id
        self.date = message.date
        self.database = dbCon
        self.jsonObj = None

    def toJSON(self):
        self.jsonObj = {
            "chat_id": self.chat_id,
            "date": self.date,
            "type": self.type,
            "is_verified": self.is_verified,
            "is_restricted": self.is_restricted,
            "is_scam": self.is_scam,
            "is_fake": self.is_fake,
            "is_support": self.is_support,
            "user": self.from_user_id
        }
        return self

    def save(self):
        try:
            if self.database:
                chatsCollection = self.database.get_collection("chats")
                if chatsCollection.find_one({"chat_id": self.chat_id}):
                    chatsCollection.update_one({"chat_id": self.chat_id}, {"$set": self.jsonObj})
                    return self
                else:
                    chatsCollection.insert_one(self.jsonObj)
                    return self
            else:
                Logs.log("Database connection error")
                return False
        except Exception as er:
            Logs.log(er)
            return False
