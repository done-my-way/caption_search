import pytube
import os
import argparse
import re


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

    lk = [line.strip('\n') for line in lk]

    return lk


def download_subs(links_list):

    base_url = 'https://www.youtube.com'

    if not os.path.exists('./subs'):
        os.mkdir('./subs')

    if not os.path.exists('./subs/xml'):
        os.mkdir('./subs/xml')

    if not os.path.exists('./subs/srt'):
        os.mkdir('./subs/srt')

    i = 1

    for url in links_list:
        yt = pytube.YouTube(base_url + url)
        title = str(yt.title)
        print(f'{i} out of {len(lk)}: {title}')
        i += 1
        caption = yt.captions.get_by_language_code('en')
        srt = caption.generate_srt_caption()
        with open('./subs/xml/{}.xml'.format(title), 'w') as f:
            f.writelines(caption)
        with open('./subs/srt/{}.srt'.format(title), 'w') as f:
            f.writelines(srt)
        with open('./subs/parsed_list.txt', 'a') as f:
            f.write(url + '\n')

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--link', help='channel or playlist URL')
    parser.add_argument('--path', help='link list file')

    args = parser.parse_args()

    if args.link:
        links = args.link + 'link'
    elif args.path:
        links = args.path + 'path'
    else:
        print('no URL provided')
        exit()

    download_subs(links)


if __name__ == '__main__':
    main()

