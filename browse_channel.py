import time

from random import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://www.youtube.com/user/khanacademy/videos"

def browse_channel(channel_url):

    browser = webdriver.Firefox()

    browser.get(url)
    time.sleep(3)

    elem = browser.find_element_by_tag_name("body")

    l = 0
    i = 0

    while len(elem.text) != l:

        print(i)
        l = len(elem.text)
        elem.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1 + 1 * random())
        i += 1



    post_elems = browser.find_elements_by_id('video-title')

    with open('./test.log', 'w') as f:
        i = 0
        for post in post_elems:
            f.write(str(i)+' '+post.text+' '+post.get_attribute('href')+'\n')
            i += 1


browse_channel(url)