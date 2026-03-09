from elasticsearch import Elasticsearch
import base64
import os



hostile = os.getenv("HOSTILE_BITS",'''R2Vub2NpZGUsV2FyIENyaW1lcyxBcGFydGhlaWQsTWFzc2FjcmUsTmFrYmEsRGlz
cGxhY2VtZW50LEh1bWFuaXRhcmlhbiBDcmlzaXMsQmxvY2thZGUsT2NjdXBhdGlvb
ixSZWZ1Z2VlcyxJQ0MsQkRT''')

less_hostile = os.getenv("LESS_HOSTILE_BITS",'''RnJlZWRvbSBGbG90aWxsYSxSZXNpc3RhbmNlLExpYmVyYXRpb24sRnJlZSBQY
Wxlc3RpbmUsR2F6YSxDZWFzZWZpcmUsUHJvdGVzdCxVTlJXQQ==''')

hostile = base64.b64decode(hostile).decode("utf-8")
less_hostile = base64.b64decode(less_hostile).decode("utf-8")

hostile = hostile.split(',') # from str to list
less_hostile = less_hostile.split(',')


es = Elasticsearch('http://localhost:9200')


index_name = "docker_test"


def set_score(record, score):
    record["bds_threat_level"] = "none"
    record["is_bds"] = False
    record["score"] = score

    match score:
        case score if score >= 75:
            record["bds_threat_level"] = "high"  
            record["is_bds"] = True
        case score if score >= 65:
            record["is_bds"] = True
            record["bds_threat_level"] = "medium"
        case score if score >= 50:
            record["bds_threat_level"] = "medium"
        
        
    return record

def calc_score(record):
        
    score = 0
    text = record["text"].lower()
    for phrase in hostile:
        if phrase.lower() in text:
            score += text.count(phrase.lower()) * 10
    for phrase in less_hostile:
        if phrase.lower() in text:
            score += text.count(phrase.lower()) * 6
    return set_score(record, score)
    
    





# README.md

# i chose the records that above 75 score to be hostile, since the avarage hostility score is 63, it seems resonable


