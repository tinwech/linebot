import requests
import random
import json
import time
from google.cloud import storage
from datetime import datetime
from config import *

storage_client = storage.Client()
bucket = storage_client.get_bucket(RESOURCE_BUCKET)
blob = bucket.blob(VIDEO_FILE)
    
def update_video():
    url = f'https://www.dcard.tw/service/api/v2/forums/funny_video/posts?popular={popular}&limit={post_num}'

    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        print('request failed')

    json_str = '[' + str(time.time()) + ',' + resp.text[1:]

    blob.upload_from_string(json_str)
    print('update success')

def get_video():
    # Download the contents of the blob as a string and then parse it using json.loads() method
    memes = json.loads(blob.download_as_string(client=None))

    #update once 12 hours
    if (time.time() - memes[0] > UPDATE_DURATION):
        update_video()

    random.seed(datetime.now())
    post = random.choice(memes[1:])
    video_url = post['mediaMeta'][1]['url']

    print('success:', video_url)
    return video_url

if __name__ == '__main__':
    update_video()