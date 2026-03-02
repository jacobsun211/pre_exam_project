from confluent_kafka import Consumer
# from shared.connection.kafka import producer
from pathlib import Path
# from db_inserter.send.elastic import insert_to_elastic
# from db_inserter.send.mongo import insert_to_mongo
import os
from shared.elastic_logger import Logger
from TTL_service.send_to_elastic import update_elastic
import speech_recognition as sr
import json

logger = Logger.get_logger()


# WRITING_TOPIC = os.getenv("TTL_SERVICE_WRITING_TOPIC1", "step2")
LISTENS_TOPIC = os.getenv("TTL_SERVICE_LISTENING_TOPIC", "extract_text")

SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


conf = {
    'bootstrap.servers': SERVER,
    'group.id': "STT",
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe([LISTENS_TOPIC])




r = sr.Recognizer()


def extract_text(record):
    audio = record["path"]
    with sr.AudioFile(audio) as audio:
        text = r.record(audio)
        text = r.recognize_google(text)
        return text
       

def main():
    while True:
        record = consumer.poll(1.0)
        if record is None: continue
        if record.error(): 
            logger.info(record.error())
            continue
        
        record = json.loads(record.value())
        record["text"] = extract_text(record)
        update_elastic(record)

main()

# python -m TTL_service.main

