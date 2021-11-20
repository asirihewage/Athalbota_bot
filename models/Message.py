from logs import Logs


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
                Logs.log("Database connection error")
                return False
        except Exception as er:
            Logs.log(er)
            return False
