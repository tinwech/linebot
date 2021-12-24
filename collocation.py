import requests
import json
from config import *

def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def getCollocation(vocabulary):
    vocabulary = vocabulary.replace("@", "")
    url = "https://linguatools-english-collocations.p.rapidapi.com/bolls/"
    querystring = {"lang":"en","query": vocabulary,"max_results":"5"}

    response = requests.request("GET", url, headers=collocatioin_headers, params=querystring)

    if response.status_code != 200:
        res = "no vocabulary"
    else:
        res = 'Collocations for ' + vocabulary + ' :\n\n'
        collocations = json.loads(response.text)
        index = 0
        for collocation in collocations:
            res += '(' + str(chr(65 + index)) + ') ' + collocation['collocation'] + '\n\n'
            i = 1
            for example in collocation['examples']:
                res += '-(' + str(i) + ') '
                res += remove_html_tags(example) + '\n\n'
                i += 1
            index += 1
            res += '\n'

    print(res)
    return res

if __name__ == '__main__':
    getCollocation('smoke')