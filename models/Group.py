from utils.Configs import Configs
from utils.Logs import log


class Group:
    def __init__(self, message, dbCon):
        self.group_id = message.chat.id
        self.type = message.chat.type
        self.date = message.date
        self.database = dbCon
        self.jsonObj = None

    def toJSON(self):
        self.jsonObj = {
            "group_id": self.group_id,
            "date": self.date,
            "type": self.type,
        }
        return self

    def save(self):
        try:
            if self.database:
                chatsCollection = self.database.get_collection("groups")
                if chatsCollection.find_one({"group_id": self.group_id}):
                    chatsCollection.update_one({"group_id": self.group_id}, {"$set": self.jsonObj})
                    return self
                else:
                    chatsCollection.insert_one(self.jsonObj)
                    return self
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def getAllGroups(self):
        try:
            if self.database:
                groupsCollection = self.database.get_collection("groups")
                if groupsCollection.count_documents({}) and groupsCollection.count_documents({}) > 0:
                    return groupsCollection.find({})
                elif groupsCollection.count_documents({}) and groupsCollection.count_documents({}) <= 0:
                    log("No groups")
                    return None
                else:
                    log("Something went wrong when fetching groups")
            else:
                log("Database connection error")
                return None
        except Exception as e:
            log(e)
            return None

    def leave(self, group_id):
        try:
            if self.database:
                answersCollection = self.database.get_collection("groups")
                if answersCollection.find_one({"group_id": int(group_id)}):
                    answersCollection.delete_one({"group_id": int(group_id)})
                    return True
                else:
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def isGroup(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({self.group_id}):
                    return True
                else:
                    return False
            return False
        except Exception as e:
            log(e)
            return False
