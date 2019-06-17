from check_updates import *
import csv
from tqdm import tqdm

# reuse downloaded files
# stop = 2000
if __name__ == '__main__':    
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
        for line in tqdm(dload[7000:]):
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
