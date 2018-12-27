import pytube
import os
import argparse
import re
from xml.etree import ElementTree as ET

def channel_links(channel_url):

    if not os.path.exists('./subs'):
        os.mkdir('./subs')

    pl = pytube.Playlist(channel_url)

    lk = pl.parse_links()

    name = re.search('.*/user/(.+)/', channel_url)

    print()

    with open(f'./subs/channel_links_{name.group(1)}.txt', 'w') as f:
        f.writelines('\n'.join(lk))

    return lk


def links_from_file(path):

    with open(path) as f:
        lk = f.readlines()

    lk = [line for line in lk]

    return lk


def download_subs(links_list):

    base_url = 'https://www.youtube.com/'

    if not os.path.exists('./subs'):
        os.mkdir('./subs')

    if not os.path.exists('./subs/xml'):
        os.mkdir('./subs/xml')

    if not os.path.exists('./subs/srt'):
        os.mkdir('./subs/srt')

    i = 1

    for url in links_list[77:]:
        print(base_url + url)
        try:
            yt = pytube.YouTube(base_url + url)
            title = str(yt.title)
            print(f'{i} out of {len(links_list)}: {title}')
            i += 1
            caption = yt.captions.get_by_language_code('en')
            with open('./subs/xml/{}.xml'.format(title), 'w') as f:
                f.write(str(caption.xml_captions))
            with open('./subs/srt/{}.srt'.format(title), 'w') as f:
                srt = caption.generate_srt_captions()
                f.writelines(srt)
            with open('./subs/parsed_list.txt', 'a') as f:
                f.write(url + '\n')
        except:
            print('smth went wrong')
            with open('./subs/error_log', 'a') as f:
                f.write(url + '\n')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--link', help='channel or playlist URL')
    parser.add_argument('--path', help='link list file')

    args = parser.parse_args()

    if args.link:
        links = channel_links(args.link)
    elif args.path:
        links = links_from_file(args.path)
    else:
        print('no URL provided')
        exit()

    #print(links)

    download_subs(links)


if __name__ == '__main__':
    main()

