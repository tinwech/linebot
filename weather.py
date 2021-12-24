import requests
import json
from config import *

Taiwan_County = ['基隆市','新北市','台北市', '臺北市','桃園市','苗栗縣','新竹市','台中市', '臺中市','彰化縣','南投縣', '雲林縣', '嘉義市', '台南市', '臺南市', '高雄市','屏東縣' ,'宜蘭縣' ,'花蓮縣' ,'台東縣', '臺東縣']

def convertLocation(location):
    for county in Taiwan_County:
        if location in county:
            location = county
            break

    if location == '台北市':
        location = '臺北市'
    elif location == '台中市':
        location = '臺中市'
    elif location == '台南市':
        location = '臺南市'
    elif location == '台東縣':
        location = '臺東縣'

    return location

def getLocalWeather(location):

    location = convertLocation(location)
    res = ''
    if location not in Taiwan_County:
        res = 'No matching location found'
        print(res)
        return res

    url = f'https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization={weather_key}&locationName={location}'
    resp = requests.get(url)
    print('status:', resp.status_code)

    if resp.status_code != 200:
        res = 'No matching location found'
        print(res)
    else:
        weatherElements = json.loads(resp.text)['records']['location'][0]['weatherElement']
        for element in weatherElements:
            name = element['elementName']
            if name == 'Wx':
                condition = element['time'][0]['parameter']['parameterName']
            elif name == 'PoP':
                rainProb = element['time'][0]['parameter']['parameterName']
            elif name == 'MinT':
                minTemp = element['time'][0]['parameter']['parameterName']
            elif name == 'MaxT':
                maxTemp = element['time'][0]['parameter']['parameterName']
            elif name == 'CI':
                ci = element['time'][0]['parameter']['parameterName']

        res = f'''{location}今天的天氣 :
{condition},{ci}

最高氣溫 : {maxTemp} °C
最低氣溫 : {minTemp} °C
降雨機率 : {rainProb} %'''

        print(res)

    return res

if __name__ == '__main__':
    location = input()
    getLocalWeather(location)
