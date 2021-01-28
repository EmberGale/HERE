import requests
import json

url = "https://www.rigla.ru/graphql"

payload="{\"query\":\"\\n        query {\\n            pvzCities{\\n              cities\\n              region_id\\n              base_url\\n              region_name\\n              default_city\\n            }\\n        }\\n      \",\"variables\":{}}"
headers = {
  'Content-Type': 'text/plain',
  'Cookie': 'PHPSESSID=9781e08c97b583dc47c700944fcb3a8a',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

#print(response.text)

j = json.loads(response.text)
j = j["data"]["pvzCities"]

#print(json.dumps(j))

ids = []
for d in j:
  ids.append(d['region_id'])

o = open("r.txt", 'w')
o.write(json.dumps(ids))
o.close 