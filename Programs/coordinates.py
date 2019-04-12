
import requests
import sys
import os


def coords_for_adress(adress):
    try:    
        request = "http://geocode-maps.yandex.ru/1.x/?format=json&geocode="
        response = None
        
        response = requests.get( request + adress )
        
        if response:
            json_response = response.json()

            toponym = json_response["response"]["GeoObjectCollection"]
            coords = toponym["featureMember"][0]["GeoObject"]["Point"]["pos"]
            coords = float( coords.split()[0] ), float( coords.split()[1] )
            
            return coords
        else:
            print( "ошибка выполнения запроса" )
            print( response.status_code, "(", response.reason, ")" )
    except Exception as ex:
        print( "НЕ удалось выполнить запрос, проверьте инет, а еще ошибка", 
               ex )
