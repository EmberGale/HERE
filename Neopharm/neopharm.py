from json import encoder
import requests
import json
import pandas as pd
import csv
import re

url= 'https://neopharm.ru/stores/all?cityId=1'

def get_data(url=None):
    if url is None:
        return False

    header = {'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest'
    }

    r = requests.get(url, headers=header)

    data = json.loads(r.text)
    
    data = data["stores"]

    return data

def format_data (data):

    geojson = {
    "type": "FeatureCollection",
    "features": [
        {
        "type": "Feature",
        "properties" : {
            "id": d["id"],
            "name": d["name"],
            "payments": [d["payments"]["card"], d["payments"]["terminal"]],
            "email": d["email"],
            "workTime": [d["workTime"]["fulltext"]],
            "allowOrder": [d["allowOrder"]["status"], d["allowOrder"]["reason"]],
            "hasRamp": d["hasRamp"],
            "hasOptics": d["hasOptics"],
            "hasOrthopedics": d["hasOrthopedics"],
            "hasCosmetics": d["hasCosmetics"],
            "hasSportFood": d["hasSportFood"],
            "hasHomeopathy": d["hasHomeopathy"],
            "hasNew": d["hasNew"],
        },
        "geometry" : {
            "type": "Point",
            "coordinates": [d['coordinates']['longitude'], d['coordinates']['latitude']],
        },
        } for value, d in data.items()]
    }

    return geojson

def main ():
    data = get_data(url)

    geojson = format_data(data)
    print('---')
    output = open("neopharm.geojson", 'w')
    json.dump(geojson, output)
    output.close()

    print('---')
    #df1 = df.loc[:, 'name':'coordinates']
    print('---')
    # Normalizing data
    scv = 'ADDRESS;ORIGINAL_LAT;ORIGINAL_LNG'
    print('---')
    for point in geojson['features']:
        s = re.sub('Аптека \d+-\d+', "", point['properties']['name'])
        s = re.sub('Аптека \d+', "", s)
        scv += f"\n{s};{point['geometry']['coordinates'][1]};{point['geometry']['coordinates'][0]}"

    print(scv)
    
    fp = open('neo.csv', 'w', encoding='utf8')
    fp.write(scv)
    fp.close

if __name__ == '__main__':
    main()