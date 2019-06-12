import subprocess
import argparse
import sys
import json
import csv
from tqdm import tqdm

def get_meta(links):
    """ """

    with open('meta_csv.csv', 'w') as f:

        fieldnames = ['id', 'title', 'duration', 'categories', 'tags', 'description', 'playlist', 'subtitles', 'automatic_captions']
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for link in tqdm(links):
            link = 'https://www.youtube.com/watch?v=' + link

            try:
                proc1 = subprocess.Popen(['youtube-dl','--write-sub', 
                '--write-auto-sub', '--skip-download', '-j', link], stdout=subprocess.PIPE)

                meta = json.loads(proc1.stdout.read())
                # save json
                with open('./meta/'+meta['id']+'.json', 'w') as f:
                    json.dump(meta, f)
                # parse to csv
                url_sub = None
                for entity in meta['subtitles']['en']:
                        if entity['ext'] == 'vtt':
                            url_sub = entity['url']
                url_cap = None
                for entity in meta['automatic_captions']['en']:
                        if entity['ext'] == 'vtt':
                            url_cap = entity['url']

                

                line = dict()

                line['id'] = meta.get('id', None)
                line['title'] = meta.get('title', None)
                line['duration'] = meta.get('duration', None)
                line['categories'] = meta.get('categories', None)
                line['tags'] = meta.get('tags', None)
                line['description'] = meta.get('description', None)
                line['playlist'] = meta.get('playlist', None)
                line['subtitles'] = url_sub
                line['automatic_captions'] = url_cap

                writer.writerow(line)

            except Exception:
                fields = ['id','title', 'title', 'duration','categories','tags','description','playlist','subtitles','automatic_captions']
                line = dict(zip(fields, [None]*len(fields)))
                writer.writerow(line)

with open('khan.txt', 'r') as f:
    links = sorted(f.read().split('\n'))
        
get_meta(links)
    
    
    
