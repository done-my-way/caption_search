from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
import srt
import os.path

es = Elasticsearch()
idx = IndicesClient(es)

mappings = {"_doc":
            {
             "properties":
             {
              "name": {"type": "text"},
              "time": {"type": "short"},
              "content": {"type": "text"}
             }
            }
           }


idx.create(index="khan_academy",
           body={"mappings": mappings})



# read file
path = '/home/wswolod/Projects/caption_search/CS/subs/srt/2d curl example.srt'

with open(path, 'r') as f:
    doc = f.read()
    body = {}
    for line in srt.parse(doc):
        body['name'] = os.path.basename(path).split('.')[0]
        body['time'] = int(line.start.total_seconds())
        body['content'] = line.content
        es.create(index="khan_academy",
                  # TODO: ids from hyperlinks
                  body=body)

# parse it

# form JSON

"""
{text: "text", str
 link: "link", str
 name: "name", str
 time: time}   float/int
"""
# push it to elastisearch storage