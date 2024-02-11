import sys
from io import BytesIO

import requests
from PIL import Image
from distance import lonlat_distance

toponym_to_find = " ".join(sys.argv[1:])

# Объект
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json",

}
response_geo = requests.get(geocoder_api_server, params=geocoder_params)

if not response_geo:
    pass

json_response = response_geo.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = map(float, toponym_coodrinates.split(" "))

# Организация
search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": f"{toponym_longitude},{toponym_lattitude}",
    "type": "biz",
    "results": "10"

}
response_org = requests.get(search_api_server, params=search_params)
if not response_org:
    pass
json_response_org = response_org.json()
print()
pharmacies = []
for i in range(min(10, json_response_org["properties"]['ResponseMetaData']["SearchResponse"]["found"])):
    pharmacy = json_response_org["features"][i]
    pharmacy_longitude, pharmacy_lattitude = pharmacy["geometry"]["coordinates"]
    info = pharmacy["properties"]["CompanyMetaData"]
    if 'Hours' in info:
        if 'круглосуточно' in info['Hours']['text']:
            ph_type = "pmrdm"
        else:
            ph_type = "pmlbm"
    else:
        ph_type = "pmgrm"
    pharmacies.append(f"{pharmacy_longitude},{pharmacy_lattitude},{ph_type}")

# Изображение
map_params = {
    "ll": f"{toponym_longitude},{toponym_lattitude}",
    "l": "map",
    "pt": f"{toponym_longitude},{toponym_lattitude},pmwtm~{'~'.join(pharmacies)}"
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(response.content)).show()
