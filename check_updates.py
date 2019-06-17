# TODO: more specific imports
import subprocess
import datetime
import json
import requests
import webvtt
from elasticsearch import Elasticsearch
import time
import datetime
import re
import csv

# TODO: channel naming
def get_list(filename):
    with open(filename, 'r') as f:
        old = sorted(f.read().split('\n'))
    return old

def check_updates(channel_link, old_list):    

    proc1 = subprocess.Popen(['youtube-dl','--flat-playlist', '-j', channel_link],stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['jq', '-r', '.id'], stdin=proc1.stdout, stdout=subprocess.PIPE)

    updates = set()

    while True:
        ID = proc2.stdout.readline()
        ID = ID.decode('utf-8')
        if not ID:
            break
        updates.add(ID)

    # TODO: channel naming
    old = get_list(old_list)

    updates = updates.difference(old)

    return updates

def get_sub(link, language='eng', format='vvt'):
    """ """
    proc1 = subprocess.Popen(['youtube-dl', '--write-sub', 
    '--write-auto-sub', '--skip-download', '-j', link], stdout=subprocess.PIPE)
    info = json.loads(proc1.stdout.read())
    title = info['title']
    ID = info['id']
    try: 
        for entity in info['subtitles']['en']:
            if entity['ext'] == 'vtt':
                url = entity['url']
    except Exception:
        try: 
            for entity in info['automatic_captions']['en']:
                if entity['ext'] == 'vtt':
                    url = entity['url']
        except Exception:
            pass
    
    text = requests.get(url).content.decode()

    return ID, title, text, info

def to_plain(ID, title, channel, vtt_file):
    lines = []
    previuos = ''
    vtt_lines = webvtt.read(vtt_file)
    text = ''

    for line in vtt_lines:
        try:
            if line != previuos:
                lines.extend(line.text.strip().splitlines())
                previuos = line
            # TODO: filter non-alphanumeric
            text = ' '.join(lines)
    

        except Exception as err:
            print(err)

    document = {'id': ID, 'name': title, 'channel': channel, 'content': text}

    return [document,]
            

def to_lines(ID, title, channel, vtt_file):
    #  TODO: do not read file
    vtt_lines = webvtt.read(vtt_file)

    number = 0
    documents = []

    for line in vtt_lines:
            try:
                if number == 0:
                    x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
                    prev_start = int(datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
                    prev_content = re.sub('\n', ' ', line.text)
                    documents.append({'id': ID, 'name': title, 'channel': channel, 'content': prev_content, 'time': prev_start})
                else:           
                    x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
                    curr_start = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
                    curr_content = re.sub('\n', ' ', line.text)    
                    midd_start = (curr_start - prev_start) // 2 + prev_start
                    midd_content = re.sub('^.*? ', '', prev_content[len(prev_content) // 2:] + ' ' + curr_content[:len(curr_content) // 2])
                    midd_content = re.match('^.* ', midd_content)[0]
                    prev_start, prev_content = curr_start, curr_content
                    documents.append({'id': ID, 'name': title, 'channel': channel, 'content': midd_content, 'time': midd_start})                    
                    documents.append({'id': ID, 'name': title, 'channel': channel, 'content': curr_content, 'time': curr_start})
                                

            except Exception as err:
                print(err)

            number += 1
        
    return documents

def push_subs(documents, connection, idx='lineswise'):
    # TODO:idx naming
    # es = Elasticsearch([{"host": host, "port": port}])
    for body in documents:
        connection.index(index=idx, doc_type='_doc', body = body)

if __name__ == '__main__':
    
    with open('channels.csv', 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            print(row)
            channel_name = row[0]
            channel_link = row[1]
            downloads = row[2]

    # old_list = 'khan.txt' # list of already processed videos
    # channel_name = 'Khan Academy'
    # channel_link = 'https://www.youtube.com/khanacademy'
    # updates = ['RSx20wLxctc']

            updates = check_updates(channel_link, downloads)
            connection = Elasticsearch([{"host": "localhost", "port": 9200}])
            for ID in updates:
                print(channel_name, ID)
                link = 'https://www.youtube.com/watch?v=' + ID
                ID, title, vtt, info = get_sub(link)

                # backups
                with open('./backup/vtt/' + ID, 'w') as f:
                    f.write(vtt)
                with open('./backup/json/' + ID, 'w') as f:
                    json.dump(info, f)

                plain_doc = to_plain(ID, title, channel_name, './backup/vtt/' + ID)
                push_subs(plain_doc, connection, 'plain')

                lines_docs = to_lines(ID, title, channel_name, './backup/vtt/' + ID)
                push_subs(lines_docs, connection, 'linewise')
                
            with open(downloads, 'a') as f:
                for ID in updates:
                    f.write(ID + '\n')