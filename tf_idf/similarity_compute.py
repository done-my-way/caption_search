import csv
import os 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

from tqdm import tqdm

# BASED ON  https://github.com/mneedham/computer-science-papers
# I'm still figuring out, how to reference other GH-projects correctly.

def find_similar(tfidf_matrix, index, top_n = 5):
    """ Finds top_n most similar documents for the 
        doc with the number "index" in tfidf_matrix. 
    """
    cosine_similarities = linear_kernel(tfidf_matrix[index:index+1], tfidf_matrix).flatten()
    related_docs_indices = [i for i in cosine_similarities.argsort()[::-1] if i != index]
    return [(index, cosine_similarities[index]) for index in related_docs_indices][0:top_n]

def collect_cropus(directory):
    """ The functions returns a corpus: a list of name-text
        pairs read from the specified directory.
    """
    corpus = []
    for filename in tqdm(os.listdir(directory)):
        with open(directory+'/'+filename, "r") as paper:
            corpus.append((filename, paper.read()))
    return corpus

def get_matrix(corpus):
    """ Returns tf-idf matrix for the given corpus.
        Vectorizer params: analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english'.
    """
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
    tfidf_matrix =  tf.fit_transform([content for filename, content in corpus])
    return tfidf_matrix

def estimate_similarities(corpus, tfidf_matrix, output_file):
    """ For each doc in the corpus computes its similarity with 
        every other. Writes down 5 closest documents for each
        into the output_file.
    """
    with open(output_file, 'w') as similarities_file:        
        with tqdm(total=len(corpus)) as pbar:
            writer = csv.writer(similarities_file, delimiter = ",")
            for doc_index, _ in enumerate(corpus):
                similar_documents =  [(corpus[index][0], score) for index, score in find_similar(tfidf_matrix, doc_index)]

                document_id = corpus[doc_index][0]

                for similar_document_id, score in similar_documents:                    
                    writer.writerow([document_id, similar_document_id, score])

                pbar.update(1)

if __name__ == "__main__":
    # collect corpus
    directory = '/home/lodya/Desktop/Projects/Term_Project_1/subs/plain'
    corpus = collect_cropus(directory)
    # compute tf-idf matrix
    tfidf_matrix = get_matrix(corpus)
    # find similar documents for each
    output_file = "/home/lodya/Desktop/Projects/Term_Project_1/caption_search/tf_idf/similarities.csv"
    estimate_similarities(corpus, tfidf_matrix, output_file)
