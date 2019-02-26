from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200}])

query = 'dot product'
res = es.search(index="khan_academy", doc_type="_doc", body={"query": {"match": {"content":{"query": f"{query}", "fuzziness": 1} }}})

for r in res['hits']['hits']:
    print(r)
    print('https://youtu.be/'+r['_source']['url'][8:]+'?t='+str(r['_source']['time']))