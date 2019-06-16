import subprocess
import json

# from pycaption import DFXPReader, WebVTTReader, WebVTTWriter
import requests


def get_subs(link, language='eng', format='vvt'):
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
    # vtt = WebVTTWriter().write(DFXPReader().read(text))

    return title, text

if __name__ == '__main__':
    link = 'https://www.youtube.com/watch?v=RSx20wLxctc'
    title, text = get_subs(link)
    with open(title + '.vtt', 'w') as f:
        f.write(text)