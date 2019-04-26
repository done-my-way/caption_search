from flask import Flask
from webpage.forms import SearchForm
from flask import request, render_template
from storage.storage_keeper import StorageKeeper
from storage.channel_downloader import download, srt_to_txt
from tf_idf.similarity_search import find_similar
from tf_idf.similarity_compute import find_similar_2
import json, srt
from tf_idf.similarity_compute import find_similar, get_matrix, collect_corpus
import re
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer

with open('tf_idf_vectorizer', 'rb') as f:
    tf_idf_vectorizer = pickle.load(f)

with open('tf_idf_matrix', 'rb') as f:
    tf_idf_matrix = pickle.load(f)

with open('corpus_index', 'rb') as f:
    corpus_index = pickle.load(f)

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
    sk = StorageKeeper(host="139.59.141.97", port=9200)
    # search the query
    search_string = str(search.data['search'])    
    search_results = sk.search_subs(search_string)
    # return the results webpage
    return render_template('results.html', query=search_string, results=search_results)

@app.route('/video')
def video():
    id = request.args['id']
    title = request.args['name']
    related = find_similar(id, './tf_idf/similarities.csv')
    texts = []
    related_names = []
    for row in related:
        with open("/home/lodya/Desktop/Projects/Term_Project_1/subs/plain/" + row[1] + '.txt') as f:
            text = f.read()
            texts.append(text[:300]+'...')
            try:
                with open("/home/lodya/Desktop/Projects/Term_Project_1/subs/mod_srt/" + row[1] + '.txt') as f_title:
                    f_title.readline()
                    f_title.readline()
                    meta_data = json.loads(f_title.readline())
                    related_names.append(meta_data['name'])
            except Exception:
                related_names.append('Title_placeholder')
    return render_template('video.html', related=related, id=id, title=title, texts=texts, related_names=related_names)

@app.route('/from_url',  methods=['GET', 'POST'])
def from_url():    
    # create search bar instance
    search = SearchForm(request.form)
    # return reulsts webpage, if search button was hit
    if request.method == 'POST':
        return search_results_url(search)
    # otherwise return the search webpage itself
    return render_template('from_url.html', form=search)

@app.route('/search_results_url')
def search_results_url(search):
    url = str(search.data['search'])
    pattern = re.compile(r'^(https://www.youtube.com/watch\?v=)')
    if re.match(pattern, url):
        # download video captions
        search_sub = download(url)
        search_sub['caption'] = srt_to_txt(search_sub['caption'])
        # look up in the corpus
        doc_vector = tf_idf_vectorizer.transform([search_sub['caption']])
        similar = find_similar_2(doc_vector, tf_idf_matrix)
        related = []
        for i in similar:
            related.append(corpus_index[i[0]])
        # render results page
        title = 'placeholder'
        texts = []
        related_names = []
        for vid in related:
            with open("/home/lodya/Desktop/Projects/Term_Project_1/subs/plain/" + vid + '.txt') as f:
                text = f.read()
                texts.append(text[:300]+'...')
                try:
                    with open("/home/lodya/Desktop/Projects/Term_Project_1/subs/mod_srt/" + vid + '.txt') as f_title:
                        f_title.readline()
                        f_title.readline()
                        meta_data = json.loads(f_title.readline())
                        related_names.append(meta_data['name'])
                except Exception:
                    related_names.append('Title_placeholder')
        return render_template('video.html', related=related, title=title, texts=texts, related_names=related_names)
    else:
        return 'not a YT-url'