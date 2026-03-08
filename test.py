from elasticsearch import Elasticsearch
import base64
hostile = '''R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlz
cGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvb
ixSZWZ1Z2VlcyxJQ0MsQkRT'''

less_hostile = '''RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQY
Wxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ=='''



es = Elasticsearch('http://localhost:9200')


result = es.ping()
print('Connected:', result)

index_name = "docker_test"











hostile = base64.b64decode(hostile).decode("utf-8")
less_hostile = base64.b64decode(less_hostile).decode("utf-8")

hostile = hostile.split(',') # from str to list
less_hostile = less_hostile.split(',')


print(hostile)
print(less_hostile)

# query_bool_example = {
#     "size": 100,
#     "query": {
#         "function_score": {
#             "query": {"match_all": {}},
#             "functions": [
#                 {"filter": {"match": {"text": hostile}}, "weight": 2.0},
#                 {"filter": {"match": {"text": less_hostile}}, "weight": 1.0}
#             ],
#             "boost_mode": "replace"
#         }
#     }}




query_bool_example = {
    "size": 100,
            "query": {"match_all": {}}        
    }

        # "should": [  # לא חייב אבל אם יש נחשב יותר
        #     {"range": {"age": {"gt": 30}}}

response = es.search(index=index_name, **query_bool_example)
records = response['hits']['hits']


sum1 = 0
hostiles = 0
for record in records:    
    score = 0
    text = record["_source"]["text"].lower()
    for phrase in hostile:
        if phrase.lower() in text:
            score += text.count(phrase.lower()) * 2
    for phrase in less_hostile:
        if phrase.lower() in text:
            score += text.count(phrase.lower()) * 1
    
    record["bds_threat_level"] = "none"
    record["is_bds"] = False
    record["score"] = score
    match score:
        case score if score >= 55:
            record["bds_threat_level"] = "medium"
        case score if score >= 75:
            record["is_bds"] = True
        case score if score >= 85:
            record["bds_threat_level"] = "high"
    
    
    print(score,'-',record["_source"]["name"],"-", record["_source"]["text"])
    print(f'hostile: {hostiles}')
    print(hostile)
    
avg1 = sum1 // 34
print(f'avg: {avg1}')





# README.md

# i chose the records that above 75 to be hostile, since the avarage hostility is 63, its seems resonable


