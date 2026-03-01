import os
from pymongo import MongoClient


class MongoConnection:
    def __init__(self):
        host = os.getenv("MONGO_HOST", "localhost")
        port = int(os.getenv("MONGO_PORT", "27017"))

       

        self.client = MongoClient(
            host,
            port
        )


client = MongoConnection().client


# import os
# from pymongo import MongoClient


# class Mongo:
#     def __init__(self):
#         host = os.getenv("MONGO_HOST", "localhost")
#         port = int(os.getenv("MONGO_PORT", "27017"))
#         self.client = MongoClient(host, port)

#         db = os.getenv("MONGO_DB", "week20")
#         self.collection = self.client[db]["records"]

        
#     def insert(self, record: dict):
#         if not self.collection.find_one({"id": record["id"]}, {"_id": 1}):
#             self.collection.insert_one(record)