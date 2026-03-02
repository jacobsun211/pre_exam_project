from pathlib import Path
from shared.connection.kafka import producer
import json
import os
from shared.elastic_logger import Logger




logger = Logger.get_logger()


WRITING_TOPIC = os.getenv("STEP1_WRITING_TOPIC", "step2")

logger.info(f"starting...")

path = Path("podcasts/")

# print(path.stat())


def send_to_kafka(record: dict):
    record = json.dumps(record)
    producer.produce(WRITING_TOPIC, record)
    producer.flush()


def metadata():
    for audio in path.iterdir():
        record = {"size": audio.stat().st_size,
                  "name": audio.name,
                  "time_created": audio.stat().st_ctime,
                  "path": str(path) + "/" +  audio.name
                  }
        send_to_kafka(record)
        logger.info(f"sent to kafka")
    
        
    
               

metadata()
print('bruh')


# python -m metadata_service.main
