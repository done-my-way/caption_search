import webvtt
import csv
from tqdm import tqdm

def to_plain(links):
    with open('plain_text.csv', 'w') as f:
        fieldnames = ['id', 'number_of_lines', 'plain_text']
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=fieldnames)
        writer.writeheader()
        for link in tqdm(links):
            try:
                lines = []
                vtt = webvtt.read('/home/lodya/Projects/Term_Project_1/caption_search/subs/' + link)
                for line in vtt:
                    lines.extend(line.text.strip().splitlines())
                text = ' '.join(lines)
                row = {'id': link,
                        'number_of_lines': len(vtt),
                        'plain_text': text}
                writer.writerow(row)
            except Exception as err:
                print(err)

with open('khan.txt', 'r') as f:
    links = sorted(f.read().split('\n'))
        
to_plain(links)