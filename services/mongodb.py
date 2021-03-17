from pymongo import MongoClient
import datetime

class DBError(Exception):
    """ raised on critical db errors """
    pass

class Database:
    client = None
    db = None
    def __init__(self, host, user, pwd, data, port=27017):
        try:
            self.client = MongoClient(f"mongodb://{user}:{pwd}@{host}:{port}/{data}")
            print(self.client)
            self.db = self.client[data]
            print(self.db)
        except:
            raise DBError("Failed to connect.")
    def insertUser(self, collection, user, fields):
        try:
            col = self.db[collection]
            doc = {"name": user, **fields}
            return col.insert_one(doc)
        except Exception as e:
            print("INSERT EXCEPTION", e)
            return None
    def updateUser(self, collection, user, fields):
        try:
            col = self.db[collection]
            res = col.update_many({"name": user}, {"$set": fields})
            return res.modified_count
        except Exception as e:
            print("UPDATE EXCEPTION", e)
            return None
    def deleteUser(self, collection, user):
        try:
            col = self.db[collection]
            res = col.delete_many({"name": user})
            return res.deleted_count
        except Exception as e:
            print("DELETE EXCEPTION", e)
            return -1
    def getUserData(self, collection, user):
        try:
            col = self.db[collection]
            res = col.find({"name": user})
            res = {}
            return res
        except Exception as e:
            print("SELECT EXCEPTION", e)
            return None
    

if __name__ == "__main__":
    HOST = ""
    PORT = 27017
    USER = ""
    PASS = ""
    DATA = ""
    db = Database(HOST, USER, PASS, DATA, PORT)
    x = db.getUserData("users", "testUser1")
    print(f"Find: {x}")
    x = db.insertUser("users", "testUser1", {"number": 3, "number2": 3.5, "addedOn": datetime.datetime.now()})
    print(f"Insert: {x}") #x.inserted_id
    x = db.getUserData("users", "testUser1")
    print(f"Find: {x}")
    x = db.updateUser("users", "testUser1", {"number": 5, "number2": 7.75})
    print(f"Update: {x}")
    x = db.getUserData("users", "testUser1")
    print(f"Find: {x}")
    x = db.deleteUser("users", "testUser1")
    print(f"Delete: {x}")
    x = db.getUserData("users", "testUser1")
    print(f"Find: {x}")
