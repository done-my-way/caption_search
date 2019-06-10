import pickle

with open('channel_dict', 'rb') as f:
    channel_dict = pickle.load(f)
with open('download_list', 'rb') as f:
    download_list = pickle.load(f)
print(len(channel_dict))