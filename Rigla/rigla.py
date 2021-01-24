import requests
import json
import selenium
from selenium import webdriver

url= 'https://www.rigla.ru/pharmacies'

def get_data(url=None):
    if url is None:
        return False

    header = {'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json, text/plain, */*',
    'X-Requested-With': 'XMLHttpRequest'
    }

#    wd = webdriver.Firefox()
#    wd.get(url)
#    ids = wd.execute_script("return sessionStorage.getItem('pvzCities')")
#    print(ids)

    s = requests.Session()
    r = requests.get(url)

    print("-GET-")
    output = open("rigla.txt", 'w')
    output.write(r.text)
    output.close()

    return True

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

if __name__ == '__main__':
    main()