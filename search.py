import sys
from io import BytesIO

import requests
from PIL import Image
from distance import lonlat_distance

import requests


def find_district(coords):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?" \
                       f"apikey=40d1649f-0493-4b70-98ba-98533de7710b" \
                       f"&geocode={coords}" \
                       f"&kind=district" \
                       f"&format=json"
    response = requests.get(geocoder_request)
    try:
        json_response = response.json()
        ans = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][4]["name"]
        return ans
    except Exception:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


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

print(find_district(toponym_coodrinates.replace(" ", ",")))
