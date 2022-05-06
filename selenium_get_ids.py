from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import json

options = Options()
options.binary_location = '/bin/firefox-developer-edition'
driver = webdriver.Firefox(options=options)
url = "https://www.youtube.com/playlist?list=PLhxUDrMFUqyMQSozC1ES-Q4BkT8MJbY_1"
driver.get(url)

elem = driver.find_element(by=By.TAG_NAME, value='html')
elem.send_keys(Keys.END)
time.sleep(3)
elem.send_keys(Keys.END)

innerHTML = driver.execute_script("return document.body.innerHTML")

page_soup = bs(innerHTML, 'html.parser')
res = page_soup.find_all('a', {'class': 'yt-simple-endpoint style-scope ytd-playlist-video-renderer'})

videos = []
for link in res:
     
    vid_id = link.get('href') 
    start = vid_id.index('?v=')
    stop = vid_id.index('&')
    vid_id = vid_id[start+3:stop]

    title = link.get('title')
    segs = title.split("|")
    if len(segs) == 1:
        segs.append('')
    videos.append({
        "id":segs[1].strip(), 
        "title":segs[0].replace("/", "-").strip(), 
        "vid_id":vid_id
        })

with open('vlogs.json', 'w') as fp:
    json.dump(videos, fp)
driver.close()

