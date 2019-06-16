# TODO: more specific imports
import subprocess
import datetime
import json
import requests
import webvtt
from elasticsearch import Elasticsearch

# TODO: channel naming
def get_list(filename='khan.txt'):
    with open(filename, 'r') as f:
        old = f.read().split('\n')
    return old

def check_updates(channel_link='https://www.youtube.com/khanacademy'):    

    proc1 = subprocess.Popen(['youtube-dl','--flat-playlist', '-j', channel_link],stdout=subprocess.PIPE)
    proc2 = subprocess.Popen(['jq', '-r', '.id'], stdin=proc1.stdout, stdout=subprocess.PIPE)

    updates = set()

    while True:
        ID = proc2.stdout.readline()
        if not ID:
            break
        updates.add(ID)

    # TODO: channel naming
    old = get_list()

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

    return ID, title, text

def to_plain(id, title, channel, vtt):

    for line in vtt:
        try:
            if line != previuos:
                lines.extend(line.text.strip().splitlines())
                previuos = line
            # TODO: filter non-alphanumeric
            text = ' '.join(lines)
            document = {'id': ID, 'name': title, 'channel': channel, 'content': text}

        except Exception as err:
            print(err)

    return [document,]
            

def to_lines():
    vtt_lines = webvtt.read()

    number = 0
    documents = []

    for line in vtt_lines:
            try:
                if number == 0:
                    x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
                    prev_start = int(datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
                    prev_content = re.sub('\n', ' ', line.text)
                    documents.append({'id': identifier, 'name': info['title'], 'channel': channel, 'content': prev_content, 'time': prev_start})
                else:           
                    x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
                    start = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
                    content = re.sub('\n', ' ', line.text)    
                    time_mid = (start - prev_start) // 2 + prev_start
                    pos_mid_prev = len(prev_content) // 2
                    pos_mid = len(content) // 2
                    content_mid = re.sub('^.*? ', '', prev_content[pos_mid_prev:] + ' ' + content[:pos_mid])
                    content_mid = re.match('^.* ', content_mid)[0]

                    documents.append({'id': identifier, 'name': info['title'], 'channel': channel, 'content': content_mid, 'time': time_mid})

                    prev_start = start
                    prev_content = content
                    
                    documents.append({'id': identifier, 'name': info['title'], 'channel': channel, 'content': content, 'time': start})                

            except Exception as err:
                print(err)

            number += 1
        
        return documents

def push_subs(documents, host="localhost", port=9200, idx='lineswise'):
    # TODO:idx naming
    es = Elasticsearch([{"host": host, "port": port}])
    for body in documents:
        es.index(index=idx, doc_type='_doc', body = body)

updates = check_updates()
for ID in updates:
    link = 'https://www.youtube.com/watch?v=' + ID
    sub = get_sub(link)