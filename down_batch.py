from down_sub import get_subs
import pickle
from pathlib import Path
import sys
import os
from multiprocessing import Pool
from tqdm import tqdm

def down_batch(download_list, range, output_path):
    """channel dict: dict with YT-identifiers and video names
       download_list: videos to download"""

    channel_dict = os.listdir(output_path)

    count = 0
    for identifier in tqdm(download_list[range]):
        count += 1
        if identifier not in channel_dict:
            try:
                link = 'https://www.youtube.com/watch?v=' + identifier
                title, text = get_subs(link)
                with open(Path(output_path, identifier + '.vtt'), 'w') as f:
                    f.write(text)
                    # channel_dict[identifier] = title
            except Exception:
                print('Error' + identifier)



if __name__ == '__main__':

    with open('khan.txt', 'r') as f:
        download_list = f.read().split('\n')
    down_batch(download_list, slice(1400, 2000), './auto_caps')
