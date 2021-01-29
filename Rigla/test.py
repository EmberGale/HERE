import requests
import json

url = "https://www.rigla.ru/graphql"

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

payload = {
	"query": "query pvzList($regionId:String, $sales:FilterTypeInput, $services:FilterTypeInput, !$groupId: String) {\n    pvzList: pvzList(\n        pageSize: 1000\n        filter: {\n            is_active: { eq: \"1\" }\n            region_id: { eq: $regionId }\n            sales: $sales\n            services: $services,\n            group_id: { eq: $groupId }\n        }\n    ) {\n        sales{\n            label\n            option_id\n        }\n        services{\n            label\n            option_id\n        }\n        items {\n            entity_id\n            name\n            region_id\n            group_name\n            group_id\n            schedule\n            latitude\n            longitude\n            address\n            phone\n            station\n            services\n            comingsoon\n        }\n    }\n}\n",
	"variables": {
		"regionId": 77,
		"sales": {},
		"services": {}
	}
}

r =requests.session()
payload = json.dumps(payload)
response = r.request("POST", url, headers=headers, data=payload)
reg_data = json.loads(response.text)


print(json.dumps(reg_data))
print("---")
print(response.status_code)

output = open("test.txt", 'w')
json.dump(reg_data, output, indent=4, sort_keys=True)
output.close()

def ToGeojson(data):
    dataGeojson = []

    for gj in data:
        my_point = geojson.Point((gj.original_lon, gj.original_lat))
        myProperties = {'url': gj.url,
                        'country': gj.country,
                        'city': gj.city,
                        'nameStore': gj.store,
                        'address': gj.address,
                        'phone': gj.phone,
                        'metroName': gj.metroName}
        feature = geojson.Feature(geometry=my_point, properties=myProperties)
        dataGeojson.append(feature)
    return geojson.FeatureCollection(dataGeojson)