import subprocess
import json

from pycaption import DFXPReader, WebVTTReader, WebVTTWriter
import requests

link = 'https://www.youtube.com/watch?v=RSx20wLxctc'


def get_subs(link, language='eng', format='vvt'):
    """ """
    proc1 = subprocess.Popen(['youtube-dl','--write-sub', 
    '--write-auto-sub', '--skip-download', '-j', link], stdout=subprocess.PIPE)
    info = json.loads(proc1.stdout.read())
    try: 
        for entity in info['subtitles']['en']:
            if entity['ext'] == 'vtt':
                url = entity['url']
    except Exception:
        for entity in info['automatic_captions']['en']:
            if entity['ext'] == 'vtt':
                url = entity['url']
    
    text = requests.get(url).content.decode()
    # vtt = WebVTTWriter().write(DFXPReader().read(text))

    return text



text = get_subs(link)
print(text)
with open('test.vtt', 'w') as f:
    f.write(text)