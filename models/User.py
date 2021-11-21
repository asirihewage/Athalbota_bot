from utils.Configs import Configs
from utils.Logs import log


class User:
    def __init__(self, message, dbCon):
        self.from_user_id = message.from_user.id
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
        self.jsonObjNew = None
        self.jsonObjUpdate = None
        self.country = None
        self.gender = None
        self.age = None
        self.translation = 2
        self.level = 0

    def toJSON(self):
        self.jsonObjUpdate = {
            "from_user_id": self.from_user_id,
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
            "language_code": self.language_code
        }
        self.jsonObjNew = {
            "from_user_id": self.from_user_id,
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
            "country": self.country,
            "gender": self.gender,
            "translation": self.translation,
            "age": self.age,
            "level": self.level
        }
        return self

    def save(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": self.jsonObjUpdate})
                    return self
                elif not self.is_restricted and not self.is_bot and not self.is_scam and not self.is_fake and self.username is not None:
                    if usersCollection.insert_one(self.jsonObjNew):
                        return self
                    else:
                        log("Failed to save user on database")
                        return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
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
            log(e)
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
            log(e)
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
            log(e)

    def makeGuest(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"level": 0}})
                    return self
                else:
                    log("Not found")
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def makeUser(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"level": 1}})
                    return self
                else:
                    log("Not found")
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def makeAdmin(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"level": 2}})
                    return self
                else:
                    log("Not found")
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def getAllUsers(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.count_documents({"level": 1}) > 0:
                    return usersCollection.find({})
                elif usersCollection.count_documents({"level": 1}) <= 0:
                    log("No users")
                    return None
                else:
                    log("Something went wrong when fetching users")
            else:
                log("Database connection error")
                return None
        except Exception as e:
            log(e)
            return None

    def getAllAdmins(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.count_documents({"level": 2}) > 0:
                    return usersCollection.find({})
                elif usersCollection.count_documents({"level": 2}) <= 0:
                    log("No admins")
                    return None
                else:
                    log("Something went wrong when fetching admins")
            else:
                log("Database connection error")
                return None
        except Exception as e:
            log(e)
            return None

    def getAllGuests(self):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.count_documents({"level": 0}) > 0:
                    return usersCollection.find({})
                elif usersCollection.count_documents({"level": 0}) <= 0:
                    log("No guests")
                    return None
                else:
                    log("Something went wrong when fetching guests")
            else:
                log("Database connection error")
                return None
        except Exception as e:
            log(e)
            return None

    def verify(self, user_id):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"username": user_id}):
                    usersCollection.update_one({"username": user_id}, {"$set": {"isVerified": True}})
                    return True
                else:
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def removeUser(self, user_id):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"username": user_id}):
                    usersCollection.update_one({"username": user_id}, {"$set": {"level": 0}})
                    return True
                else:
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def promoteAdmin(self, user_id):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"username": user_id}):
                    usersCollection.update_one({"username": user_id}, {"$set": {"level": 2}})
                    return True
                else:
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def removeAdmin(self, user_id):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"username": user_id}):
                    usersCollection.update_one({"username": user_id}, {"$set": {"level": 1}})
                    return True
                else:
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def setTranslation(self, translation):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"translation": translation}})
                    return self
                else:
                    log("Not found")
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def setGender(self, gender):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"gender": gender}})
                    return self
                else:
                    log("Not found")
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def setCountry(self, country):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"country": country}})
                    return self
                else:
                    log("Not found")
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False

    def setAge(self, age):
        try:
            if self.database:
                usersCollection = self.database.get_collection("users")
                if usersCollection.find_one({"from_user_id": self.from_user_id}):
                    usersCollection.update_one({"from_user_id": self.from_user_id}, {"$set": {"age": int(age)}})
                    return self
                else:
                    log("Not found")
                    return False
            else:
                log("Database connection error")
                return False
        except Exception as er:
            log(er)
            return False
