from elasticsearch import Elasticsearch

if __name__ == '__main__':

    host="localhost"
    port=9200

    es = Elasticsearch([{"host": host, "port": port}])

    settings =  {"settings" :
                    {
                    "index" :
                        {
                            "number_of_shards" : 1, 
                            "number_of_replicas" : 1 
                        }
                    }
                }

    mapping_1 = {"_doc":
                    {
                    "properties":
                        {
                        "channel": {"type": "keyword"},
                        "id": {"type": "keyword"},
                        "name": {"type": "text"},
                        "time": {"type": "short"},
                        "content": {"type": "text"}
                        }
                    }
               }
    es.indices.create('linewise', {"mappings": mapping_1, "setings": settings})

    mapping_2 = {"_doc":
                    {
                    "properties":
                        {
                        "channel": {"type": "keyword"},
                        "id": {"type": "keyword"},
                        "name": {"type": "text"},
                        "content": {"type": "text"}
                        }
                    }
                }
    es.indices.create('plain', {"mappings": mapping_2, "setings": settings})
    
