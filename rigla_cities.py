import requests

url = "https://www.rigla.ru/graphql"

payload="{\"query\":\"\\n        query {\\n            pvzCities{\\n              cities\\n              region_id\\n              base_url\\n              region_name\\n              default_city\\n            }\\n        }\\n      \",\"variables\":{}}"
headers = {
  'Content-Type': 'text/plain',
  'Cookie': 'PHPSESSID=9781e08c97b583dc47c700944fcb3a8a'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)