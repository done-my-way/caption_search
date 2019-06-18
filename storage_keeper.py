from elasticsearch import Elasticsearch

class StorageKeeper:

    def __init__(self, host="localhost", port=9200):
        self.es = Elasticsearch([{"host": host, "port": port}])
    
    def search_subs(self, search_phrase, idx="khan_academy"):
        """ Searches for the given search_phrase in the given index (full-text SEARCH).
            Returns top-n matches.
        """        
        body = {"query":{"match":{"content":{"query": f"{search_phrase}", "fuzziness": "AUTO"}}}}

        res = self.es.search(index=idx, doc_type="_doc", body=body)
        return res

    def search_text_by_id(self, search_phrase, idx):
        """ """        
        body = {"query": {"term": {"id": {"value": f"{search_phrase}"}}}}

        res = self.es.search(index=idx, doc_type="_doc", body=body)
        
        return res

    def search_similar_texts(self, search_phrase, idx):
        """ """        
        body = {"query": {"match": {"content": {"query":f"{search_phrase}"}}}}

        res = self.es.search(index=idx, doc_type="_doc", body=body)
        
        return res
