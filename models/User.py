from logs import Logs


class User:
    def __init__(self, message, dbCon):
        self.from_user_id = message.from_user.id
        self.is_self = message.from_user.is_self
        self.is_contact = message.from_user.is_contact
        self.is_mutual_contact = message.from_user.is_mutual_contact
        self.is_deleted = message.from_user.is_deleted
        self.is_bot = message.from_user.is_bot
        self.is_verified = message.from_user.is_verified
        self.is_restricted = message.from_user.is_restricted
        self.is_scam = message.from_user.is_scam
        self.is_fake = message.from_user.is_fake
        self.is_support = message.from_user.is_support
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name
        self.status = message.from_user.status
        self.username = message.from_user.username
        self.language_code = message.from_user.language_code
        self.database = dbCon
        self.jsonObj = None
        self.country = None
        self.gender = None
        self.age = None

    def toJSON(self):
        self.jsonObj = {
            "from_user_id": self.from_user_id,
            "is_self": self.is_self,
            "is_contact": self.is_contact,
            "is_mutual_contact": self.is_mutual_contact,
            "is_deleted": self.is_deleted,
            "is_bot": self.is_bot,
            "is_verified": self.is_verified,
            "is_restricted": self.is_restricted,
            "is_scam": self.is_scam,
            "is_fake": self.is_fake,
            "is_support": self.is_support,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "status": self.status,
            "username": self.username,
            "language_code": self.language_code,
            "gender": self.gender,
            "country": self.country,
            "age": self.age
        }
        return self

    def save(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": self.jsonObj})
                    return self
                else:
                    if usersCollection.insert_one(self.jsonObj):
                        return self
                    else:
                        Logs.log("Failed to save user on database")
                        return False
            else:
                Logs.log("Database connection error")
                return False
        except Exception as er:
            Logs.log(er)
            return False

    def isGuest(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id, 'level': 0}):
                    return True
                else:
                    return False
            return False
        except Exception as e:
            Logs.log(e)
            return False

    def isUser(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id, 'level': 1}):
                    return True
                else:
                    return False
            return False
        except Exception as e:
            Logs.log(e)
            return False

    def isAdmin(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id, "level": 2}):
                    return True
                else:
                    return False
            return False
        except Exception as e:
            Logs.log(e)

    def makeGuest(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"level": 0}})
                    return self
                else:
                    if usersCollection.insert_one(self.jsonObj):
                        return self
                    else:
                        Logs.log("Failed to save user on database")
                        return False
            else:
                Logs.log("Database connection error")
                return False
        except Exception as er:
            Logs.log(er)
            return False

    def makeUser(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"level": 1}})
                    return self
                else:
                    if usersCollection.insert_one(self.jsonObj):
                        return self
                    else:
                        Logs.log("Failed to save user on database")
                        return False
            else:
                Logs.log("Database connection error")
                return False
        except Exception as er:
            Logs.log(er)
            return False

    def makeAdmin(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"level": 2}})
                    return self
                else:
                    if usersCollection.insert_one(self.jsonObj):
                        return self
                    else:
                        Logs.log("Failed to save user on database")
                        return False
            else:
                Logs.log("Database connection error")
                return False
        except Exception as er:
            Logs.log(er)
            return False
