import pygame
import random
import requests
import sys
import os


from map import map_for_coords



coords = input("ВВедите координаты (не судите строго, я сделаю нормально)\nс пробелом без зпт: ").split()
COORDS = [float(coords[0]), float(coords[1])]
SCALE = 1

pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = "map.png"


map_for_coords(COORDS, SCALE,"map")

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
