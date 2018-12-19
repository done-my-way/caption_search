import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get("https://www.youtube.com/user/SocraticaStudios/videos")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 1

while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.1)
    no_of_pagedowns-=1

post_elems = browser.find_elements_by_id('video-title')

for post in post_elems:
    print(post.text,  end=' ')
    print(post.get_attribute('href'))