from elasticsearch import Elasticsearch
import os

host = os.getenv("ELASTICSEARCH_HOST", "http://localhost")
port = os.getenv("ELASTICSEARCH_PORT", "9200")

# ! the actual connection !
es = Elasticsearch(f"{host}:{port}")

index_name = os.getenv("ELASTIC_INDEX", "docker_test2")

mapping = {
    "properties": {
        "size":         {"type": "integer"},
        "name":         {"type": "keyword"},
        "time_created": {"type": "integer"},
        "path":         {"type": "keyword"},
        "id":           {"type": "keyword"}
    }
}


if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, mappings=mapping)
    print(f"Created index '{index_name}'")





def insert_to_elastic(record: dict):
    es.update(
        index=index_name,
        id=record["id"],
        body={
            "doc": record,
            "doc_as_upsert": True  # creates if not exists, updates if it does
        }
    )


# pip install "elasticsearch<9,>=8.0.0"

