from confluent_kafka import Consumer
from pathlib import Path
from shared.connection.kafka import producer
from db_inserter.send.elastic import insert_to_elastic
from db_inserter.send.mongo import insert_to_mongo
import hashlib
import json
import os
from shared.elastic_logger import Logger

logger = Logger.get_logger()


WRITING_TOPIC = os.getenv("INSERTER_WRITING_TOPIC", "extract_text")
LISTENS_TOPIC = os.getenv("INSERTER_LISTENING_TOPIC", "step2")

SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")



conf = {
    'bootstrap.servers': SERVER,
    'group.id': "db inserter",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])


    
def send_to_kafka(record: dict):
    logger.info(record)
    record = json.dumps(record)
    producer.produce(WRITING_TOPIC, record)
    producer.flush()


def add_id(record):
    path = Path(record["path"])
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
        send_to_kafka(record)
        logger.info(f"sent {record["name"]} kafka, in topic: {WRITING_TOPIC}")
        



listener()

# python -m db_inserter.main
