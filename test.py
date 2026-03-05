from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import base64
hostile = '''R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlz
cGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvb
ixSZWZ1Z2VlcyxJQ0MsQkRT'''

less_hostile = '''RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQY
Wxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=='''


# hostile_list = base64.b64decode(hostile)
# less_hostile = base64.b64decode(less_hostile)
# hostile_list = hostile_list.decode("utf-8")
# less_hostile = less_hostile.decode("utf-8")
# # hostile_list = hostile_list.decode("utf-8").split(', ')
# less_hostile_list = [term.strip() for term in less_hostile.split(',')]
# hostile_list = [term.strip() for term in hostile_list.split(',')]


es = Elasticsearch('http://localhost:9200')


result = es.ping()
print('Connected:', result)

index_name = "docker_test"




# response = es.search(index=index_name, body={})

# response['hits']['hits'] is a list of the matching documents.
# Each item has '_source' with the document data.






hostile = base64.b64decode(hostile).decode("utf-8")
less_hostile = base64.b64decode(less_hostile).decode("utf-8")




query_bool_example = {
    "size": 100,
    "query": {
        "function_score": {
            "query": {"match_all": {}},
            "functions": [
                {"filter": {"match": {"text": hostile}}, "weight": 2.0},
                {"filter": {"match": {"text": less_hostile}}, "weight": 1.0}
            ],
            "boost_mode": "replace"
        }
    }}




query_bool_example = {
    "size": 100}



response = es.search(index=index_name, **query_bool_example)


records = response['hits']['hits']

hostiles = 0
for record in records:    
    score = 0
    for word in record["_source"]["text"].split():
        if word in hostile:
            score += 2
        if word in less_hostile:
            score += 1
    if score >= 50:
        hostiles += 1
    # print(record["_source"]["name"],"-", record["_source"]["text"])
    print(score,'-',record["_source"]["name"])
    print(f'hostile: {hostiles}')
    
    


# Genocide,War Crimes,Apartheid,Massacre,Nakba,Displacement,Humanitarian Crisis,Blockade,Occupation,Refugees,ICC,BDS

