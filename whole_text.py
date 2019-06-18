from elasticsearch import Elasticsearch

class StorageKeeper:

    def __init__(self, host="localhost", port=9200):
        self.es = Elasticsearch([{"host": host, "port": port}])
    
    
    def search_text_by_id(self, search_phrase, idx):
        """ Searches for the given search_phrase in the given index (full-text SEARCH).
            Returns top-n matches.
        """        
        body = {"query": 
                {
                    "match": 
                    {
                        "id":
                        {
                            "query": f"{search_phrase}"
                        }
                    }
                }
               }

        res = self.es.search(index=idx, doc_type="_doc", body=body)
        
        return res

    def search_similar texts(self, search_phrase, idx):
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
        
        return res


a = StorageKeeper()
res = a.search_subs('cYyfwJSvT-k', idx='plain')
text = res['hits']['hits'][0]['_source']['content']
print(text)
res2 = a.search_subs_1(text, idx='plain')
for i in res2['hits']['hits']:
    print(i['_source']['id'])
    print(i['_source']['content'][:256])