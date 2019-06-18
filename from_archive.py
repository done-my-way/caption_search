from check_updates import *
import csv
from tqdm import tqdm

if __name__ == '__main__':
    # reuse downloaded files from previous iterations
    range_from = 0
    range_to = 1000

    channel_name = 'Khan Academy'
    count = 0 
    connection = Elasticsearch([{"host": "localhost", "port": 9200}])
    with open('./EDA_old/meta_csv.csv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        next(reader, None)
        dload =[]
        for line in reader:
            if line[0] != '':
                dload.append(line)
        for line in tqdm(dload[range_from:range_to]):
            count += 1            
            ID = line[0]
            title = line[1]
            print(ID)
            if ID:
                vtt_file = './backup/vtt/' + ID
                try:
                    plain_doc = to_plain(ID, title, channel_name, vtt_file)
                    push_subs(plain_doc, connection, 'plain')

                    lines_docs = to_lines(ID, title, channel_name, vtt_file)
                    push_subs(lines_docs, connection, 'linewise')
                except Exception as err:
                    print(err)
