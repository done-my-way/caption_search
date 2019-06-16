from elasticsearch import Elasticsearch
import srt 
import os
import json

from tqdm import tqdm

import subprocess

class StorageKeeper:

    def __init__(self, host="localhost", port=9200):
        self.es = Elasticsearch([{"host": host, "port": port}])
    
    def push_subs(self, file, idx="khan_academy"):
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
                self.es.index(index=idx, doc_type='_doc', body = body)
    
    def search_subs(self, search_phrase, idx="khan_academy"):
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
        

        hits = []

        for r in res['hits']['hits']:
            # TODO: delete score
            score = r['_score']
            vid_name = r['_source']['name']
            snippet_text = r['_source']['content'].strip(':;.,/?-[]\{\}()').lower()
            # snippet_url = 'https://www.youtube.com/embed/'+r['_source']['url'][8:]+'?start='+str(r['_source']['time'])
            snippet_url = r['_source']['id']
            if r['_source'].get('time', False):
                start_time = str(r['_source']['time'])
                hits.append((score, vid_name, snippet_text, snippet_url, start_time))
            else:
                hits.append((score, vid_name, snippet_text, snippet_url))
        return hits

def create_index(host="localhost", port=9200):

    es = Elasticsearch([{"host": host, "port": port}])

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
        return None
        # es.indices.delete("khan_academy")
    
    es.indices.create("khan_academy", {"mappings": mappings})

def batch_upload(host="localhost", port=9200, idx="khan_academy", directory='../subs'):
    sk = StorageKeeper(host=host, port=port)
    for file in tqdm(os.listdir(directory)):
        #print(file)
        try:
            sk.push_subs(directory+file, idx=idx)
        except Exception as err:
            print(err)

if __name__=="__main__":
    #create_index(host="139.59.141.97", port=9200)
    #batch_upload(host="139.59.141.97", port=9200, idx="khan_academy", directory='../subs/')
    # sk  = StorageKeeper(host="139.59.141.97", port=9200)
    # batch_upload(host="139.59.141.97", port=9200, idx="khan_academy", directory='../subs/mod_srt/')
    phrase_1 = "[instructor] in this video, we're going to dig a little bit deeper and try to understand how we might multiply larger and larger numbers. in particular, we're gonna focus on multiplying two-digit numbers times one-digit numbers. so, i always encourage you pause this video, and see if you can have a go at this. try to see if you can figure out what 37 times six is with some type of method. all right, now let's try to come up with a method ourselves. one way to think about it is the different places. this three is in the tens place, so it represents three tens, and this seven is in the ones place, so it represents seven ones. so, you can break up the 37 right over here as three tens. i'll write it like this. three tens plus, plus, and i'll do this in yellow, seven ones. and then, we are going to multiply that times six. now, another way you could think about this, this is the same thing as, i could rewrite this as, three tens is the same thing as 30, and seven ones is, of course, just the same thing as seven times six. and, you could also view this, and you could call the distributive property if you like, or i really want you to think about it, why it's intuitive. if i have 37 sixes, that's the same thing as 30 sixes, 30 sixes plus seven sixes, plus seven sixes, and i'll put the parentheses there just so we can keep track. once again, 37 of something is equal to 30 of that something plus seven of that something. 37 times six is 30 times six plus seven times six. then, we could figure these out. what is 30 times six? well, three times six is 18, so three tens times six is going to be 18 tens which is the same thing as 180, and seven times six is 42. we just then need to add these two numbers, and we could think about them in terms of the different places. we could look at the ones place, zero ones, two ones, so that'll give us two ones. then, we can think in terms of the tens place, so we have four tens and eight tens, so that is going to be 12 tens. we could write that down as 120. then, we only have 100 right over here, so we don't have a hundreds place over here, so i'll do 100, and if you add these together, 100 plus 120, you add the hundreds, you get 220. then, you add the two ones. you get 222. so, this is all going to be equal to 222. now, this isn't the only way to approach it. we could actually try to do it kind of like this, but we could write things so it's a little bit easier to keep track of. so, i could write, let me write it this way, 37 times six. i'll have you, this column here is where i want to write my ones places, and this column here is where i wanna write my tens places, and if hundreds places show up, i'll write it over there. that's just really to keep track of things. then, i can do the same thing. i could take my six, and i could say all right, this is the same thing as three tens times six plus seven ones times six. and, i could do it in either order. let's do the ones first. so if i do the seven ones times six, that's going to be 42, four tens plus two ones. how did i get that? that is seven ones times six or seven sixes. that's how i got this number here. then, we could multiply our three tens times the six which we did over here, so three tens times six. well, that's 30 sixes which we already know is 180. one in the hundreds place, eight tens, zero ones. now, this makes it a little bit easier to add everything together. exactly what we did at this step right over here. everything is in the right place value, so it's easy to add them up. two ones plus zero ones is going to be two ones. four tens plus eight tens is 12 tens or 102 tens, so i could put the two tens here and then put that 100 up here, and then 100 plus 100 is 200. so, there you have it, 222. the whole point here though is to really appreciate what is going on. that we're just breaking up the 37. we're breaking up this two-digit number into its places, the three tens, the seven ones, and then we're multiplying each of those times the six in this situation, and we did it both ways. these are just different ways to write the same, really the same method"
    phrase_2 = 'dot product'
    sk = StorageKeeper()
    res = sk.search_subs(phrase_2, idx='linewise')
    print(res)