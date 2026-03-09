from elasticsearch import Elasticsearch
import os
from shared.elastic_logger import Logger

logger = Logger.get_logger()



host = os.getenv("ELASTICSEARCH_HOST", "http://localhost")
port = os.getenv("ELASTICSEARCH_PORT", "9200")

es = Elasticsearch(f"{host}:{port}")

index_name = os.getenv("ELASTIC_INDEX", "docker_test")


mapping = {
                "properties":{
                    "bds_percent":      { "type":"float" },
                    "is_bds":           {"type":"boolean"},
                    "bds_threat_level": {"type":"keyword"}
                }
            }
es.indices.put_mapping(index=index_name,body=mapping)

def update_elastic(record: dict):
    
    
    es.update( # OR you could use this if you dont want to update _score directly
        index=index_name,
        id=record["id"],
        body={
            "doc": record,
            "doc_as_upsert": True 
        }
    )

    

    logger.info(f'sent to elastic: {record["name"]}')
