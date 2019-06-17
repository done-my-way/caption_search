import argparse
import csv
import sys
import os
import  pathlib

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--channel-name', dest='name')
    parser.add_argument('--channel-link', dest='link')
    parser.add_argument('--archive-name', dest='arch', help='name of a file to index downloaded videos')
    args = parser.parse_args()

    headers = ['name', 'link', 'downloads']
    fields = [args.name, args.link, args.name]
    channel = dict(zip(headers, fields))

    if not os.path.isfile('channels.csv'):
        with open('channels.csv', 'w') as f: 
            writer = csv.DictWriter(f, headers, delimiter = '\t')
            writer.writerow(channel)
            # create a file to store the downloads list
            with open(args.name, 'x') as d:
                pass
    else:
        with open('channels.csv', 'a') as f:
            writer = csv.DictWriter(f, headers)
            writer.writerow(channel)