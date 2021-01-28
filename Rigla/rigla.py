import requests
import json

url = "https://www.rigla.ru/graphql"

headers = {
  'Content-Type': 'text/plain',
  'Cookie': 'PHPSESSID=9781e08c97b583dc47c700944fcb3a8a',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

# Get region ids
def get_ids(url=None, payload=None):
  if url is None:
    return False
  
  if payload is None:
    return False

  response = requests.request("POST", url, headers=headers, data=payload)

  #Take block with cities and regions
  j = json.loads(response.text)
  j = j["data"]["pvzCities"]

  # Make region id list
  ids = []
  for d in j:
    ids.append(d['region_id'])

  return ids

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

#Get data for each region
for reg_id in ids:
  payload = {"query":"query pvzList($regionId:String, $sales:FilterTypeInput, $services:FilterTypeInput, !$groupId: String) {\n    pvzList: pvzList(\n        pageSize: 1000\n        filter: {\n            is_active: { eq: \"1\" }\n            region_id: { eq: $regionId }\n            sales: $sales\n            services: $services,\n            group_id: { eq: $groupId }\n        }\n    ) {\n        sales{\n            label\n            option_id\n        }\n        services{\n            label\n            option_id\n        }\n        items {\n            entity_id\n            name\n            region_id\n            group_name\n            group_id\n            schedule\n            latitude\n            longitude\n            address\n            phone\n            station\n            services\n            comingsoon\n        }\n    }\n}\n","variables":{"regionId":reg_id,"sales":{},"services":{}}}
  response = requests.request("POST", url, headers=headers, data=payload)
  reg_data = json.loads(response.text)



o = open("r.txt", 'w')
o.write(json.dumps(ids))
o.close 

def main ():
  payload="{\"query\":\"\\n        query {\\n            pvzCities{\\n              cities\\n              region_id\\n              base_url\\n              region_name\\n              default_city\\n            }\\n        }\\n      \",\"variables\":{}}"

  id_list = get_ids(url, payload)

  geojson = format_data(data)
  output = open("neopharm.geojson", 'w')
  json.dump(geojson, output)
  output.close()

if __name__ == '__main__':
    main()