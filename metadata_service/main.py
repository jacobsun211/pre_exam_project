from pathlib import Path
from shared.connection.kafka import producer
import json
import os
from shared.elastic_logger import Logger
from datetime import datetime



logger = Logger.get_logger()


WRITING_TOPIC = os.getenv("METADATA_SERVICE_WRITING_TOPIC", "step2")


logger.info(f"starting...")

path = Path("podcasts/")

# print(path.stat())
# all stats of the file!, not of the path

def send_to_kafka(record: dict):
    record = json.dumps(record)
    producer.produce(WRITING_TOPIC, record)
    producer.flush()

               

def metadata():
    for audio in path.iterdir():
        record = {"size": audio.stat().st_size,
                  "name": audio.name,
                   "time_created": datetime.fromtimestamp(audio.stat().st_ctime).isoformat(),  # ← ISO!
                  "path": str(path) + "/" +  audio.name
                  }
        send_to_kafka(record)
        logger.info(f"sent to kafka")
    
        # "time_created": audio.stat().st_ctime,
    
               

metadata()


# python -m metadata_service.main
