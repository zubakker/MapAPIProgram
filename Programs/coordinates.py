
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

def get_ll_span(address):
    toponym = requests.get("http://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + address).json()["response"]["GeoObjectCollection"]["featureMember"]
    if not toponym:
        return (None,None)
    toponym = toponym[0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и Широта :
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
 
    # Собираем координаты в параметр ll
    ll = ",".join([toponym_longitude, toponym_lattitude])
 
    # Рамка вокруг объекта:
    envelope = toponym["boundedBy"]["Envelope"]
 
    # левая, нижняя, правая и верхняя границы из координат углов:
    l,b = envelope["lowerCorner"].split(" ")
    r,t = envelope["upperCorner"].split(" ")
  
    # Вычисляем полуразмеры по вертикали и горизонтали
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
 
    # Собираем размеры в параметр span
    span = "{dx},{dy}".format(**locals())
 
    return (ll, span)
