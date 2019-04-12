import requests
import sys
import os


def map_for_coords(coords, scale, tp):
    coords = str(coords[0]) + "," + str(coords[1])
    
    scale = 5 / scale
    response = None
    try:
        map_request = "https://static-maps.yandex.ru/1.x/?&l={}&spn={},{}&ll=".format( tp, scale, scale )
        response = requests.get( map_request + coords )
     
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request + coords)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except Exception as ex:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет., А еще ", ex)
        sys.exit(1)
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

