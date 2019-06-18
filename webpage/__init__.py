from flask import Flask
from webpage.forms import SearchForm
from flask import request, render_template
from storage_keeper import StorageKeeper
import json, srt
import re


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():

    """Search webpage."""
    
    # create search bar instance
    search = SearchForm(request.form)
    # return reulsts webpage, if search button was hit
    if request.method == 'POST':
        return search_results(search)
    # otherwise return the search webpage itself
    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):

    """ Search results webpage."""

    # connect to the database
    sk = StorageKeeper(host="localhost", port=9200) #"139.59.141.97"
    # search the query
    search_string = str(search.data['search'])    
    res = sk.search_subs(search_string, idx='linewise')
    hits = []
    for r in res['hits']['hits']:
        vid_name = r['_source']['name']
        snippet_text = r['_source']['content']
        snippet_url = r['_source']['id']
        start_time = str(r['_source']['time'])
        hits.append((vid_name, snippet_text, snippet_url, start_time))
    search_results = hits
    # return the results webpage
    return render_template('results.html', query=search_string, results=search_results)

@app.route('/video')
def video():

    """Similar videos webpage."""

    ID = request.args['id']
    sk = StorageKeeper(host="localhost", port=9200)
    res = sk.search_text_by_id(ID, idx='plain')
    text = re.sub(r'\W+', ' ', res['hits']['hits'][0]['_source']['content'])
    title = res['hits']['hits'][0]['_source']['name']
    res2 = sk.search_similar_texts(text[:1024], idx='plain')
    related_ids = []
    texts = []
    related_titles = []
    for i in res2['hits']['hits']:
        related_ids.append(i['_source']['id'])
        texts.append(i['_source']['content'][:256])
        related_titles.append(i['_source']['name'])
    return render_template('video.html', related=related_ids, id=ID, title=title, texts=texts, related_names=related_titles)

