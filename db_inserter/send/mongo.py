from shared.connection.mongo import client
from bson import Binary


db = client["week20"]
collection = db["records"]



def insert_to_mongo(record):
    if not collection.find_one({"id": record["id"]}):
        with open(record["path"], "rb") as audio:
            collection.insert_one({
                "id":record["id"],
                "file": Binary(audio.read()) # to insert audio to mongo, this has limit of 16mb tho
            })