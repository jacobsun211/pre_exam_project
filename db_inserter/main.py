from confluent_kafka import Consumer
from pathlib import Path
from db_inserter.send.elastic import insert_to_elastic
from db_inserter.send.mongo import insert_to_mongo
import hashlib
import json
import os
from shared.elastic_logger import Logger

logger = Logger.get_logger()

LISTENS_TOPIC = os.getenv("INSERTER_LISTENING_TOPIC", "step2")

SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


conf = {
    'bootstrap.servers': SERVER,
    'group.id': "db inserter",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])


    


def add_id(record):
    path = Path(record["path"])
    print(path)
    with open(path, "rb") as f:
        id = hashlib.file_digest(f, "sha256")
    return id.hexdigest() # hexa for str only id, use digest for binary id ;)



def listener():
    logger.info(f"started listening on topic {LISTENS_TOPIC}")
    while True:
        record = consumer.poll(1.0)
        if record is None: continue
        if record.error(): 
            logger.info(record.error())
            continue
        
        logger.info(f"got massage")
        record = json.loads(record.value())
        id = add_id(record) # creating unique id based on the file content
        record["id"] = id
        insert_to_mongo(record) # inserting to mongo if its not already there
        logger.info(f"sent {record["name"]} to mongo")
        insert_to_elastic(record) # likewise for elastic
        logger.info(f"sent {record["name"]} to elastic")
        print(record)
        print('noice')



listener()

# python -m db_inserter.main
