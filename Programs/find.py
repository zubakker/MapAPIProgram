import requests
import sys
import os

from math import sqrt
from distance import lonlat_distance

def addr_for_coords(coords):
    toponym = requests.get("http://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + coords).json()["response"]["GeoObjectCollection"]["featureMember"]
    if not toponym:
        return "", ""
    top = toponym[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]
    if "postal_code" in top["Address"]:
        return top["text"], top["Address"]["postal_code"]
    return top["text"], ""

def org_for_coords(coords, COORDS):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"


    address_ll = str(coords[0]) + "," + str(coords[1])


    search_params = {
        "apikey": api_key,
        "lang": "ru_RU",
        "spn": "0.001,0.001",
        "rspn": "1",
        "ll": coords,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()
    #print("------")
    for i in range( len(json_response["features"]) ):
        organization = json_response["features"][i]
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        point = organization["geometry"]["coordinates"]
        #print(lonlat_distance(point, COORDS), org_address, point[0]-COORDS[0], point[1]-COORDS[1])
        if lonlat_distance(point, COORDS) <= 50:
            point = str(point[0]) + "," + str(point[1])
            return org_name + "," + org_address
    return ""


"""

all_shops = list()

for i in range( min(10, len(json_response["features"])) ):
    organization = json_response["features"][i]
    
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    
    tim = organization["properties"]["CompanyMetaData"]["Hours"]
    point = organization["geometry"]["coordinates"]
    point = str(point[0]) + "," + str(point[1])
    

    if "Availabilities" in tim and "TwentyFourHours" in tim["Availabilities"][0]:
        all_shops.append( [point, 1] )
        
    elif "Availabilities" in tim and "Intervals" in tim["Availabilities"][0]:
        all_shops.append( [point, 2] )
    else:
        all_shops.append( [point, 0] )
            
    [36.286565, 54.498455] [36.286814965221595, ]


"""

