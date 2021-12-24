from datetime import datetime
import time
import requests
import random
import json
from bs4 import BeautifulSoup
from google.cloud import storage
from config import *

storage_client = storage.Client()
bucket = storage_client.get_bucket(RESOURCE_BUCKET)
blob = bucket.blob(BEAUTY_FILE)

def updateBeauty():
  ptt_url = 'https://www.ptt.cc'
  resp = requests.get('https://www.ptt.cc/bbs/Beauty/index.html', cookies={'over18':'1'})    # 傳送 Cookies 資訊後，抓取頁面內容
  soup = BeautifulSoup(resp.text, "html.parser")   
  u = soup.select("div.btn-group.btn-group-paging a")
  last_page_url = ptt_url + u[1]["href"]
  resp = requests.get(last_page_url, cookies={'over18':'1'})
  soup = BeautifulSoup(resp.text, "html.parser")   

  post_urls = []
  date_divs = soup.find_all('div', 'r-ent')
  for d in date_divs:
    push_count = d.find('div', 'nrec').text
    print(push_count)
    if push_count and not push_count.startswith('X') and (push_count == '爆' or int(push_count) >= 10):
      if d.find('a'):
        href = d.find('a')['href']
        post_urls.append(href)

  img_urls = '[' + str(time.time())
  for post_url in post_urls:
    resp = requests.get(ptt_url + post_url, cookies={'over18':'1'})
    soup = BeautifulSoup(resp.text, "html.parser")   
    imgs = soup.find_all('img')
    for img in imgs:
      if '.gif' not in img['src']:
        img_urls += ',"' + img['src'] + '"'
  img_urls += ']'
  blob.upload_from_string(img_urls)
  
def getBeauty():
  random.seed(datetime.now())
  if random.randint(1, 10) != 1:
    return random.choice(antihorny_url)

  beauty = json.loads(blob.download_as_string(client=None))
  #update once 6 hours
  if (time.time() - beauty[0] > UPDATE_DURATION):
    updateBeauty()

  img_url = random.choice(beauty[1:])

  print('success:', img_url)
  return img_url