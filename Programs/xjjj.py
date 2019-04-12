import pygame
import random
import requests
import sys
import os


from map import map_for_coords



coords = input("ВВедите координаты (не судите строго, я сделаю нормально)\nс пробелом без зпт: ").split()
COORDS = [float(coords[0]), float(coords[1])]
SCALE = 1.0

pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = "map.png"


map_for_coords(COORDS, SCALE,"map")

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                SCALE *= 1.8
                if SCALE > 3000:
                    SCALE = 3000
            
            elif event.key == pygame.K_PAGEDOWN:
                SCALE /= 1.8
                if 10 / SCALE > abs(90 - COORDS[0]) or 10 / SCALE > abs(-90 - COORDS[0]) or \
                   10 / SCALE > abs(180 - COORDS[1]) or 10 / SCALE > abs(-180 - COORDS[0]):
                    SCALE = max(  5 / abs(90 - COORDS[0]),
                                  5 / abs(-90 - COORDS[0]),
                                  5 / abs(180 - COORDS[0]),
                                  5 / abs(-180 - COORDS[0]) )
                
            map_for_coords(COORDS, SCALE, "map")
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
