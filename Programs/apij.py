import pygame
import random
import requests
import sys
import os

from distance import lonlat_distance
from funcion import scale_for_response
from coordinates import coords_for_adress

pygame.init()
screen = pygame.display.set_mode((600, 450))

map_file = "map.png"

cities = [ "Москва", "Калуга", "Воронеж", "Рязань", "Полярные Зори",
           "Тотьма", "Благовещенск", "Тамбов", "Пермь" ]

def next_slide(coords):
    coords = str(coords[0]) + "," + str(coords[1])

    response = None
    tp = random.choice( ["sat", "map"] )
    try:
        map_request = "https://static-maps.yandex.ru/1.x/?&l={}&spn=0.01,0.01&ll=".format( tp )
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

city = random.choice(cities)
next_slide( coords_for_adress( city ) )

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove(map_file)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            city = random.choice(cities)
            next_slide( coords_for_adress( city ) )
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


