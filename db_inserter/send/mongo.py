from shared.connection.mongo import client
import gridfs


db = client["week20"]
collection = db["records"]

fs = gridfs.GridFS(db)


def insert_to_mongo(record):
    id = record["id"]
    if db.fs.files.find({"_id": id}) is None: # chaecking if mongo has this record, if it does - insert to mongo
        with open(record["path"], "rb") as audio:
            fs.put(audio,_id=record["id"],filename=record["name"])
            


# for records that are > 16MB, using binary

# from bson import Binary
# def insert_to_mongo(record):
#     if not collection.find_one({"id": record["id"]}):
#         with open(record["path"], "rb") as audio:
#             collection.insert_one({
#                 "id":record["id"],
#                 "file": Binary(audio.read()) # to insert audio to mongo, this has limit of 16mb tho
#             })