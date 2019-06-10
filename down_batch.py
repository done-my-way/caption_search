from down_sub import get_subs
import pickle
from pathlib import Path
import sys
import os
from multiprocessing import Pool

def down_batch(download_list_path, output_path):
    """channel dict: dict with YT-identifiers and video names
       download_list: videos to download"""

    # with open(channel_dict_path, 'rb') as f:
    #     channel_dict = pickle.load(f)

    channel_dict = os.listdir(output_path)

    with open(download_list_path, 'rb') as f:
        download_list = pickle.load(f)

    count = 0
    for identifier in download_list[5935:]:
        count += 1
        # sys.stdout.write(str(count) + ' out of ' + str(len(download_list)) + ' ' + identifier)
        # sys.stdout.flush()
        # print()
        if identifier not in channel_dict:
            try:
                link = 'https://www.youtube.com/watch?v=' + identifier
                title, text = get_subs(link)
                with open(Path(output_path, identifier + '.vtt'), 'w') as f:
                    f.write(text)
                    # channel_dict[identifier] = title
            except Exception:
                print('Error' + identifier)

    with open(channel_dict_path, 'wb') as f:
        pickle.dump(channel_dict, f)

def pool_adapter(identifier):
    channel_dict = os.listdir('/home/lodya/Projects/Term_Project_1/caption_search/new_subs')
    count = 0
    # for identifier in download_list:
    #     count += 1
    #     sys.stdout.write(str(count) + ' out of ' + str(len(download_list)) + ' ' + identifier)
    #     sys.stdout.flush()
    #     # print()
    if identifier not in channel_dict:
        try:
            link = 'https://www.youtube.com/watch?v=' + identifier
            title, text = get_subs(link)
            with open(Path('./new_subs', identifier + '.vtt'), 'w') as f:
                f.write(text)
                sys.stdout.write(identifier)
                sys.stdout.flush()
                # channel_dict[identifier] = title
        except Exception:
            print('Error' + identifier)

    # with open(channel_dict_path, 'wb') as f:
    #     pickle.dump(channel_dict, f)    

if __name__ == '__main__':

    down_batch('download_list', './new_subs')

# with open('khan.txt', 'r') as f:
#     download_list = []
#     line = ' '
#     while line:
#         line = f.readline()
#         download_list.append(line)
#     with open('channel_dict', 'wb') as f:
#         pickle.dump(download_list, f)

# with open('channel_dict', 'wb') as f:
#     d = dict()
#     pickle.dump(d, f)