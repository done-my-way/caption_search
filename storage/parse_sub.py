import os
import json

import webvtt

import time
import datetime

import re

def parse_sub(identifier, title, channel, body):
    """ """
    pass
    
def push_subs(file):

    body = {}
    body['id'] = ''
    body['name'] = ''
    body['channel'] = ''
    srt_lines = webvtt.read(file)
    number = 0
    for line in srt_lines:
        if number == 0:
            x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
            prev_start = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
            prev_content = re.sub('\n', ' ', line.text)

            body['content'] = prev_content
            body['time'] = prev_start
            print(prev_start, prev_content)

        else:           
            x = time.strptime(line.start.split('.')[0],'%H:%M:%S')
            start = int(datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds())
            content = re.sub('\n', ' ', line.text)    
            time_mid = (start - prev_start) // 2 + prev_start
            pos_mid_prev = len(prev_content) // 2
            pos_mid = len(content) // 2
            content_mid = re.sub('^.*? ', '', prev_content[pos_mid_prev:] + ' ' + content[:pos_mid])
            content_mid = re.match('^.* ', content_mid)[0]

            print('mid', time_mid, content_mid)
            body['content'] = content_mid
            body['time'] = time_mid

            prev_start = start
            prev_content = content

            print(start, content)
            body['content'] = content
            body['time'] = start

        number += 1

if __name__ == '__main__':
    push_subs('test.vtt')