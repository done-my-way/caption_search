from elasticsearch import Elasticsearch
import srt 
import os
import json

class StorageKeeper:

    def __init__(self, host="localhost", port=9200):
        self.es = Elasticsearch([{"host": host, "port": port}])
    
    def push_subs(self, file, index):
        """ Works with modified .srt files.
            Creates a document for EVERY LINE in the subtitles.

            The 0's entry contains metadata.
            0
            00:00:00,000 --> 00:00:00,000
            {"url":"url", "name":"name"}
        """
        body = {}
        with open(file, 'r') as f:
            srt_lines = srt.parse(f.read())
        meta_data = json.loads(next(srt_lines).content)
        body['url'] = meta_data['url']
        body['name'] = meta_data['name']
        for line in srt_lines:
            body['time'] = int(line.start.total_seconds())
            body['content'] = line.content
            print(self.es.index(index=index, doc_type='_doc', body = body))
    
    def search_subs(self, search_phrase, index):
        """ Searches for the given search_phrase in the given index (full-text SEARCH).
            Returns top-n matches.
        """        
        body = {"query": 
                {
                    "match": 
                    {
                        "content":
                        {
                            "query": f"{search_phrase}", 
                            "fuzziness": 1
                        } 
                    }
                }
               }

        res = self.es.search(index=index, doc_type="_doc", body=body)

        hits = []

        for r in res['hits']['hits']:
            vid_name = r['_source']['name'])
            snippet_text = r['_source']['text']
            snippet_url = 'https://youtu.be/'+r['_source']['url'][8:]+'?t='+str(r['_source']['time']))
            hits.append((vid_name, snippet_text, snippet_url))
        
        return hits

def create_index():

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

# path = './subs/srt/'

# with open('./logs/in_storage.log', 'r') as f:
#     in_storage = f.readlines()
#     in_storage = [line for line in in_storage]

# for file in os.listdir('./subs/srt'):
#     if os.path.isfile(path+file) and (file not in in_storage):
#         with open('./logs/in_storage.log', 'a') as f:
#             f.write(file+'\n')
#         print(file)
#         try:
#             with open(path+file, 'r') as f:
#                 doc = f.read()
#                 body = {}
#                 for line in srt.parse(doc):
#                     body['url'] = file.split('.')[0].split('*')[0]
#                     body['name'] = file.split('.')[0].split('*')[1]
#                     body['time'] = int(line.start.total_seconds())
#                     body['content'] = line.content
#                     es.index(index="khan_academy", doc_type='_doc', body=body)
#         except Exception as err:
#             with open('./logs/storage_keeper.log', 'a') as f:
#                 f.write(str(err)+'\n')

if __name__ == '__main__':

    sk = StorageKeeper()
    sk.push_subs('test_modified_srt.srt', 1)
