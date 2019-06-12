import os
import json

import webvtt

import time
import datetime

import re

from elasticsearch import Elasticsearch

from tqdm import tqdm

from pathlib import Path

import subprocess


class StorageKeeper:

    def __init__(self, host="localhost", port=9200):
        self.es = Elasticsearch([{"host": host, "port": port}])
    
    def push_subs(self, path, identifier, channel, idx):

        body = {}

        body['id'] = identifier
        
        link = 'https://www.youtube.com/watch?v=' + identifier
        proc1 = subprocess.Popen(['youtube-dl', '--skip-download', '-j', link], stdout=subprocess.PIPE)
        info = json.loads(proc1.stdout.read())
        body['name'] = info['title']

        # TODO: allow channel name changes
        body['channel'] = channel

        file = Path(path, identifier)
        vtt_lines = webvtt.read(file)
        number = 0

        with open('id_names.txt', 'a') as f:
            f.write(identifier + '\t' + body['name'] + '\n')

        for line in vtt_lines:
            try:
                if number == 0:
                    x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
                    prev_start = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
                    prev_content = re.sub('\n', ' ', line.text)

                    body['content'] = prev_content
                    body['time'] = prev_start
                    self.es.index(index=idx, doc_type='_doc', body = body)


                else:           
                    x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
                    start = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
                    content = re.sub('\n', ' ', line.text)    
                    time_mid = (start - prev_start) // 2 + prev_start
                    pos_mid_prev = len(prev_content) // 2
                    pos_mid = len(content) // 2
                    content_mid = re.sub('^.*? ', '', prev_content[pos_mid_prev:] + ' ' + content[:pos_mid])
                    content_mid = re.match('^.* ', content_mid)[0]

                    
                    body['content'] = content_mid
                    body['time'] = time_mid
                    self.es.index(index=idx, doc_type='_doc', body = body)


                    prev_start = start
                    prev_content = content

                    body['content'] = content
                    body['time'] = start
                    self.es.index(index=idx, doc_type='_doc', body = body)
                    

            except Exception as err:
                print(err)

            number += 1
    
    def search_subs(self, search_phrase, idx):
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
                            "fuzziness": "AUTO"
                        }
                    }
                }
               }

        res = self.es.search(index=idx, doc_type="_doc", body=body)
        
        logging.debug(str(res))

        hits = []

        for r in res['hits']['hits']:
            vid_name = r['_source']['name']
            snippet_text = r['_source']['content'].strip(':;.,/?-[]\{\}()').lower()
            # snippet_url = 'https://www.youtube.com/embed/'+r['_source']['url'][8:]+'?start='+str(r['_source']['time'])
            snippet_url = r['_source']['url']
            start_time = str(r['_source']['time'])
            hits.append((vid_name, snippet_text, snippet_url, start_time))
        
        return hits

def create_index(name, host="localhost", port=9200):

    es = Elasticsearch([{"host": host, "port": port}])

    mappings = {"_doc":
                {
                "properties":
                {
                "channel": {"type": "text"},
                "url": {"type": "text"},
                "name": {"type": "text"},
                "time": {"type": "short"},
                "content": {"type": "text"}
                }
                }
            }

    # if es.indices.exists("khan_academy"):
    #     return None
    #     # es.indices.delete("khan_academy")
    
    es.indices.create(name, {"mappings": mappings})

def batch_upload(host, port, idx, directory, file_range, channel):
    sk = StorageKeeper(host=host, port=port)
    for file in tqdm(sorted(os.listdir(directory))[file_range]):
        identifier = file.split('.')[0].strip()
        # print(identifier)
        try:
            sk.push_subs(directory, identifier, channel, idx)
        except Exception as err:
            print(err)

# from threading import Thread, Lock

# class DatabaseWorker(Thread):
#     __lock = Lock()

#     def __init__(self, db, query, result_queue):
#         Thread.__init__(self)
#         self.db = db
#         self.query = query
#         self.result_queue = result_queue

#     def run(self):
#         result = None
#         try:
#             conn = connect(host=host, port=port, database=self.db)
#             curs = conn.cursor()
#             curs.execute(self.query)
#             result = curs
#             curs.close()
#             conn.close()
#         except Exception as e:
#             logging.error("Unable to access database %s" % str(e))
#         self.result_queue.append(result)

# delay = 1
# result_queue = []
# worker1 = DatabaseWorker("db1", "select something from sometable", result_queue)
# worker2 = DatabaseWorker("db1", "select something from othertable", result_queue)
# worker1.start()
# worker2.start()

# # Wait for the job to be done
# while len(result_queue) < 2:
#     sleep(delay)
# job_done = True
# worker1.join()
# worker2.join()

if __name__=="__main__":
    #create_index(host="139.59.141.97", port=9200)
    #batch_upload(host="139.59.141.97", port=9200, idx="khan_academy", directory='../subs/')
    # sk  = StorageKeeper(host="139.59.141.97", port=9200)
    # batch_upload(host="139.59.141.97", port=9200, idx="khan_academy", directory='../subs/mod_srt/')
    
    # create new common index for all channels
    # create_index('subtitle_search', host="139.59.141.97", port=9200)
    # push subs for the Khan Academy
    file_range = slice(0, 1000)
    batch_upload(host="139.59.141.97", port=9200, idx='subtitle_search',
    directory='./subs', file_range=file_range, channel='Khan Academy')
    # for file in os.listdir('./new_subs'):
    #     with open('./new_subs/'+file, 'r') as f:
    #         text = f.read()
    #     ID = file.split('.')[0].strip()
    #     print(ID)
    #     with open('./subs/'+ID, 'w') as f:
    #         text = f.write(text)
