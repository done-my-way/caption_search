import srt
import os

from tqdm import tqdm

def srt_to_plain(input_filename, output_filename):
    """
    """
    try:
        with open(input_filename, 'r') as inp:
            subs = srt.parse(inp.read())
            plain_text = ''
            for line in subs:
                plain_text += line.content + ' '
        with open(output_filename, 'w') as out:
            out.write(plain_text)
    except Exception as err:
        print(input_filename, '\n', err)

def srt_to_modified(input_filename, output_filename, link, name):
    """
    """
    with open(input_filename, 'r') as inp:
        text = inp.read()

    modification = [
                    '0\n',
                    '00:00:00,000 --> 00:00:00,000\n',
                    '{"url":"'+link+'", "name":"'+name+'"}\n',
                    '\n'
                    ]

    with open(output_filename, 'w') as out:
        out.writelines(modification)
        out.write(text)

def batch_conversion(dir_path_in, dir_path_out, mod_fnct):
    """
    """
    docs = os.listdir(dir_path_in)

    if not os.path.isdir(dir_path_out):
        os.mkdir(dir_path_out)
        
    for doc in tqdm(docs):
        new_filename = doc.split('*')[0][10:]
        mod_fnct(dir_path_in+'/'+doc, dir_path_out+'/'+new_filename+'.txt')


def batch_conversion_2(dir_path_in, dir_path_out):
    """
    """
    docs = os.listdir(dir_path_in)

    if not os.path.isdir(dir_path_out):
        os.mkdir(dir_path_out)
        
    for doc in tqdm(docs):
        link = doc.split('*')[0][10:]
        name = doc.split('*')[1].split('.')[0]
        srt_to_modified(dir_path_in+'/'+doc, dir_path_out+'/'+link+'.txt', link, name)


inp = '/home/lodya/Desktop/Projects/Term_Project_1/subs/srt'
out = '/home/lodya/Desktop/Projects/Term_Project_1/subs/mod_srt'
batch_conversion_2(inp, out)