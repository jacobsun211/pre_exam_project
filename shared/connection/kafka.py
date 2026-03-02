import os
from confluent_kafka import Producer
from shared.elastic_logger import Logger

logger = Logger.get_logger()
import time

logger.info('sleeping for 10 sec')
time.sleep(10)

class KafkaConnection:
    def __init__(self):
        SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.producer = Producer({"bootstrap.servers": SERVER})


producer = KafkaConnection().producer
