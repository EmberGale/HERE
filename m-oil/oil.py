
import requests
import json
from bs4 import BeautifulSoup
import lxml
import re

url = "http://m-oil.ru/map/"

def sort(data):
    
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
            "type": "Feature",
            "properties" : {
                'id': feature['id'],
                    'name': feature['label'],
                    'address': feature['address'],
                    'se_tyres_restore': feature['se_tyres_restore'], 
                    'se_extra_clean': feature['se_extra_clean'], 
                    'se_vacuum': feature['se_vacuum'], 
                    'se_coffee': feature['se_coffee'], 
                    'se_terminal': feature['se_terminal'], 
                    'se_gas': feature['se_gas'], 
                    'se_three_d': feature['se_three_d'], 
                    'se_coffe_baked': feature['se_coffe_baked'], 
                    'fu_dt': feature['fu_dt'], 
                    'fu_80': feature['fu_80'], 
                    'fu_92': feature['fu_92'], 
                    'fu_95': feature['fu_95'], 
                    'fu_ai-100': feature['fu_ai-100'], 
                    'fu_gaz': feature['fu_gaz'], 
                    'pa_qiwi': feature['pa_qiwi'], 
                    'pa_gazprom': feature['pa_gazprom'], 
                    'pa_magistral': feature['pa_magistral'], 
                    'pa_magnatek': feature['pa_magnatek'], 
                    'pa_aris': feature['pa_aris'], 
                    'pa_inforcom': feature['pa_inforcom'], 
                    'pa_scanoil': feature['pa_scanoil'], 
                    'pa_clubauto': feature['pa_clubauto'], 
                    'pa_petrol': feature['pa_petrol'], 
                    'pa_cards': feature['pa_cards'], 
                    'pa_talon': feature['pa_talon'], 
                    'pa_terminal-service': feature['pa_terminal-service'], 
                    'pa_e100': feature['pa_e100'], 
                    'pa_ballami-spasibo': feature['pa_ballami-spasibo'], 
                    'pa_rosneft-card': feature['pa_rosneft-card']
            },
            "geometry" : {
                "type": "Point",
                "coordinates": [float(feature['longitude']), float(feature['latitude'])]
            },
            } for feature in data]
        }

    return geojson

def get_data (url):
    
    response = requests.get(url) 
    
    soup = BeautifulSoup(response.text, 'lxml')

    scripts = soup.findAll('script')
    
    for index, script in enumerate(scripts):
        
        script_content = script.string
        if script_content is not None and "Map.Data.stations =" in script_content:
            
            match = re.search(r"Map.Data.stations = \[(.+)\]", str(script_content))
            
            data = json.loads(match.group(0).split('=')[1])

            return data

def main ():
    data = get_data(url)
    print(data)
    data = sort(data)
    o = open("oil.geojson", 'w')
    o.write(json.dumps(data))
    o.close

if __name__ == '__main__':
    main()