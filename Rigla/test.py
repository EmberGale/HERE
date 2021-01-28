import requests
import json

url = "https://www.rigla.ru/graphql"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0",
}

payload = {
	"query": "query pvzList($regionId:String, $sales:FilterTypeInput, $services:FilterTypeInput, !$groupId: String) {\n    pvzList: pvzList(\n        pageSize: 1000\n        filter: {\n            is_active: { eq: \"1\" }\n            region_id: { eq: $regionId }\n            sales: $sales\n            services: $services,\n            group_id: { eq: $groupId }\n        }\n    ) {\n        sales{\n            label\n            option_id\n        }\n        services{\n            label\n            option_id\n        }\n        items {\n            entity_id\n            name\n            region_id\n            group_name\n            group_id\n            schedule\n            latitude\n            longitude\n            address\n            phone\n            station\n            services\n            comingsoon\n        }\n    }\n}\n",
	"variables": {
		"regionId": 77,
		"sales": {},
		"services": {}
	}
}
payload = json.dumps(payload)
response = requests.request("POST", url, headers=headers, data=payload)
reg_data = json.loads(response.text)

print(json.dumps(reg_data))

output = open("test.txt", 'w')
json.dump(reg_data, output)
output.close()