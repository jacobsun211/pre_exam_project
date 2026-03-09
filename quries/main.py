from fastapi import FastAPI
from elasticsearch import Elasticsearch
import os

host = os.getenv("ELASTICSEARCH_HOST", "http://localhost")
port = os.getenv("ELASTICSEARCH_PORT", "9200")
index_name = os.getenv("ELASTIC_INDEX","records")

es = Elasticsearch(f"{host}:{port}")

app = FastAPI()



@app.get('/')
def get_all():
    records = es.search(index=index_name, body={"size":100})
    response = []
    for record in records["hits"]["hits"]:
        response.append(record["_source"])
    return "results found", len(response),response



@app.get('/by_threat/')
def get_threat():
    try:
        print('yoink')
        records = es.search(index="records", body={"query": {"term": {"bds_threat_level": "medium"}},
                                                   "_source":["name","bds_threat_level"]}) # optional, to get only these fields and not all the document
        records = records['hits']['hits']
        return "results found", len(records),records
    except Exception as e:
        return {"error": str(e)}
    







