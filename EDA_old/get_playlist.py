import subprocess
import argparse
import sys


def get_playlist(link, out_file):
    """ """
    proc1 = subprocess.Popen(['youtube-dl','--flat-playlist', '-j', link],stdout=subprocess.PIPE)
    # filters json with "jq" to get the "id" field
    proc2 = subprocess.Popen(['jq', '-r', '.id'], stdin=proc1.stdout, stdout=subprocess.PIPE)
    count = 0
    # write the output to the speciefied file
    with open(out_file, 'w') as f:
        # line by line
        while True:
            line = proc2.stdout.readline()
            if not line:
                break
            f.write(line.decode('utf-8'))
            count += 1
            # to immediately write to the stdout
            sys.stdout.write(str(count) + ' ' +line.decode('utf-8'))
            sys.stdout.flush()

#  get_playlist('https://www.youtube.com/playlist?list=PLmKbqjSZR8TZmG4vFnBIIH35EWswFgsG0', 'test_list.txt')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('channel_link', help='A link to the channel you want to list')
    parser.add_argument('output_file', help='A file path to write the list')
    args = parser.parse_args()
    get_playlist(args.channel_link, args.output_file)