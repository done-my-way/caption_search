import requests
from bs4 import BeautifulSoup
import re

rq = requests.get('https://www.youtube.com/user/TheYoungTurks/videos')

soup = BeautifulSoup(rq.text, 'lxml')
links = soup.find_all('a')
print([a['href'] for a in links if re.search('^/watch', a['href'])])

