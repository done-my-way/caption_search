from flask import Flask
from WebPage.forms import SearchForm
from flask import request, render_template
from storage.storage_keeper import StorageKeeper

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
    sk = StorageKeeper()
    # search the query
    search_string = str(search.data['search'])    
    search_results = sk.search_subs(search_string)
    # return the results webpage
    return render_template('results.html', query=search_string, results=search_results)
