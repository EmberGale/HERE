import requests
import json
import pandas as pd
import traceback, sys, code


API_KEY = "d9iIt3blT6x2EM3QInT8_cB4V0HZv7wetmpQoT-AHfA"
url = "https://www.rigla.ru/graphql"
# File no_coords.geojson created for addresses that couldn't be geocoded
no_coords = []

# Geocode 'coming soon' addresses
def geocode (address, apiKey):
    
    # Основной домен сервиса геокодирования
    URL = 'https://geocode.search.hereapi.com/v1/geocode'
    
    # Параметры запроса
    params = {
        'q': address,
        'apiKey': apiKey
    }
    
    # Парсинг ответа в JSON формате
    response = requests.get(URL, params=params).json()
    try:
      item = response['items'][0]
    except:
      result = {
        'lat': None,
        'lng': None,
      }
      return result

    address = item['address']
    position = item['position']

    result = {
        'address': address['label'],
        'lat': position['lat'],
        'lng': position['lng'],
    }
    
    return result

# Get region ids
def get_ids(url, payload, headers):
  if url is None:
    return False
  
  if payload is None:
    return False

  response = requests.request("POST", url, headers=headers, data=payload)

  # Take block with cities and regions
  j = json.loads(response.text)
  j = j["data"]["pvzCities"]

  # Make region id list
  ids = []
  for d in j:
    ids.append(d['region_id'])

  return ids

# Merge geojson data
def ToGeojson(data, dataGeojson):

  for d in data:
    if d["comingsoon"] == '0':
      if d['address'] == '':
        continue
      
      print("Coming soon: ", d["address"])
      buff = geocode(d['address'], API_KEY)
      d['longitude'] = buff['lat']
      d['longitude'] = buff['lng']
      
    if d['longitude'] == None:
      no_coords.append(
        {"name": d["name"],
			  "address": d["address"],
			  "phone": d["phone"],
			  "schedule": d["schedule"],
        "comingsoon": d["comingsoon"]})
      continue
    
    geojson = {
			"type": "Feature",
			"properties" : {
			"name": d["name"],
			"address": d["address"],
			"phone": d["phone"],
			"schedule": d["schedule"],
      "comingsoon": d["comingsoon"]
		},
			"geometry" : {
			"type": "Point",
			"coordinates": [float(d['longitude']), float(d['latitude'])],
		}
		}
    dataGeojson.append(geojson)
  
  return dataGeojson

#Get data for each region
def proc_ids(url, headers, ids):
  reg_data = None
  p_geojson = []
  #ids = [75]
  print(ids)
    
  for reg_id in ids:
    # Change payload to get date for each region
    print(reg_id)
    payload = {
      "query": "query pvzList($regionId:String, $sales:FilterTypeInput, $services:FilterTypeInput, !$groupId: String) {\n    pvzList: pvzList(\n        pageSize: 1000\n        filter: {\n            is_active: { eq: \"1\" }\n            region_id: { eq: $regionId }\n            sales: $sales\n            services: $services,\n            group_id: { eq: $groupId }\n        }\n    ) {\n        sales{\n            label\n            option_id\n        }\n        services{\n            label\n            option_id\n        }\n        items {\n            entity_id\n            name\n            region_id\n            group_name\n            group_id\n            schedule\n            latitude\n            longitude\n            address\n            phone\n            station\n            services\n            comingsoon\n        }\n    }\n}\n",
      "variables": {
        "regionId": int(reg_id),
        "sales": {},
        "services": {}
      }
    }
    payload = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(response.text)
    data = data["data"]["pvzList"]["items"]
    
    output = open("test.txt", 'w')
    output.write(json.dumps(data, indent=4, sort_keys=True))
    output.close()

    #Convert into geojson
    reg_data = ToGeojson(data, p_geojson)
    reg_data = {
        "type": "FeatureCollection",
        "features": reg_data
    }

  return reg_data

def main ():
  headers = {
    'Content-Type': 'text/plain',
    'Cookie': 'PHPSESSID=9781e08c97b583dc47c700944fcb3a8a',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
  }
  payload="{\"query\":\"\\n        query {\\n            pvzCities{\\n              cities\\n              region_id\\n              base_url\\n              region_name\\n              default_city\\n            }\\n        }\\n      \",\"variables\":{}}"
  # Get region/ city ids  
  id_list = get_ids(url, payload, headers)
  # Without header -> response = 500
  headers = {
    'Host': 'www.rigla.ru',
    'Connection': 'keep-alive',
    'Content-Length': '900',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.473',
    'X-APP': 'WEB',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Origin': 'https://www.rigla.ru',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.rigla.ru/pharmacies',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': '_gcl_au=1.1.773306477.1611860284; _ga=GA1.2.528943024.1611860284; _gid=GA1.2.712967600.1611860284; _ym_uid=1611860285577036092; _ym_d=1611860285; _ym_visorc=w; _ym_isad=2; quoteId=a95eeb225d02beebd62d8988e4204d7b; regionSuggested=1; PHPSESSID=55bd367a2e5748b49a3af916340ac6e7; _gat_UA-37163999-1=1; _gat_UA-37163999-6=1; _gat_UA-37163999-7=1'
  }

  geo = []
  geo = proc_ids(url, headers, id_list)

  output = open("rigla.geojson", 'w')
  json.dump(geo, output)
  output.close()
  # Failde to get coords
  output = open("no_coords.geojson", 'w')
  json.dump(no_coords, output)
  output.close()

if __name__ == '__main__':
    main()