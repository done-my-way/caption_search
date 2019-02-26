from elasticsearch import Elasticsearch
import srt
import os

es = Elasticsearch()

mappings = {"_doc":
            {
             "properties":
             {
              "url": {"type": "text"},
              "name": {"type": "text"},
              "time": {"type": "short"},
              "content": {"type": "text"}
             }
            }
           }

if es.indices.exists("khan_academy"):
    es.indices.delete("khan_academy")

es.indices.create("khan_academy", {"mappings": mappings})

path = './subs/srt/'

with open('./logs/in_storage.log', 'r') as f:
    in_storage = f.readlines()
    in_storage = [line for line in in_storage]

for file in os.listdir('./subs/srt'):
    if os.path.isfile(path+file) and (file not in in_storage):
        with open('./logs/in_storage.log', 'a') as f:
            f.write(file+'\n')
        print(file)
        try:
            with open(path+file, 'r') as f:
                doc = f.read()
                body = {}
                for line in srt.parse(doc):
                    body['url'] = file.split('.')[0].split('*')[0]
                    body['name'] = file.split('.')[0].split('*')[1]
                    body['time'] = int(line.start.total_seconds())
                    body['content'] = line.content
                    es.index(index="khan_academy", doc_type='_doc', body=body)
        except Exception as err:
            with open('./logs/storage_keeper.log', 'a') as f:
                f.write(str(err)+'\n')

