import requests
import random
import json
import time
from datetime import datetime
from google.cloud import storage
from config import *

storage_client = storage.Client()
bucket = storage_client.get_bucket(RESOURCE_BUCKET)
blob = bucket.blob(MEME_FILE)
    
def update_meme():
    url = f'https://www.dcard.tw/service/api/v2/forums/meme/posts?popular={popular}&limit={post_num}'

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print('request failed')

    json_str = '[' + str(time.time()) + ',' + resp.text[1:]

    blob.upload_from_string(json_str)
    print('update success')

def get_meme():
    # Download the contents of the blob as a string and then parse it using json.loads() method
    memes = json.loads(blob.download_as_string(client=None))

    #update once 12 hours
    if (time.time() - memes[0] > UPDATE_DURATION):
        update_meme()

    random.seed(datetime.now())
    post = random.choice(memes[1:])
    img_url = post['mediaMeta'][0]['url']

    print('success:', img_url)
    return img_url
