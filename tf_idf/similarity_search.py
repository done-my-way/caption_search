import csv

def find_closest(similartities_table_file, N):
    """ Returns a list of the documents with the 
        highest tf-idf score in the corpus used to 
        build the similarity table.
    """
    items = []
    with open(similartities_table_file, "r") as similarities_file:
        reader = csv.reader(similarities_file, delimiter=",")
        for row in reader:
            lst = list(row)
            lst[-1] = float(lst[-1])
            items.append(tuple(lst))
    by_similarity = sorted(items, key = lambda x: x[-1], reverse=True)
    return by_similarity[:N]

def find_similar(doc_id, similartities_table_file):
    """ The file id should be specified in the form
        used in the similartities_table_file.
        The 0's column in the similarities_table_file
        should be a document identificator (doc_id).
    """
    results = []
    with open(similartities_table_file, 'r') as sim_file:
        reader = csv.reader(sim_file, delimiter=',')
        for row in reader:
            if row[0] == doc_id:
                results.append(row)
    return results


if __name__ == '__main__':
    # find closest subtitle files
    similarity_table = "/home/lodya/Desktop/Projects/Term_Project_1/caption_search/tf_idf/similarities.csv"
    closest = find_closest(similarity_table, 10)
    for row in closest:
        print(row)
    # find similar to aSZhNFEOE.txt (vid about vectors) files
    similar  = find_similar('aSZhNFEOE.txt', similarity_table)
    for row in similar:
        print(row)
