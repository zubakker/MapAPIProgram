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

Font = pygame.font.SysFont("courier new", 20)
map_for_coords(COORDS, SCALE,"map")

tp = 0
types = ["map", "skl", "sat"]
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                SCALE *= 2
                if SCALE > 3000:
                    SCALE = 3000
            
            elif event.key == pygame.K_PAGEDOWN:
                SCALE /= 2
                if 2.5 / SCALE > abs(90 - COORDS[0]) or 2.5 / SCALE > abs(-90 - COORDS[0]) or \
                   2.5 / SCALE > abs(180 - COORDS[1]) or 2.5 / SCALE > abs(-180 - COORDS[0]):
                    SCALE = max(  2.5 / abs(90 - COORDS[0] - 0.00000001),
                                  2.5 / abs(-90 - COORDS[0] - 0.00000001),
                                  2.5 / abs(180 - COORDS[0] - 0.00000001),
                                  2.5 / abs(-180 - COORDS[0] - 0.00000001) )
                
            elif event.key == pygame.K_LEFT:
                COORDS[0] -= 5 / (3.1 * SCALE) + 180
                COORDS[0] = COORDS[0] % 360 - 180
            
            elif event.key == pygame.K_RIGHT:
                COORDS[0] += 5 / (3.1 * SCALE) + 180
                COORDS[0] = COORDS[0] % 360 - 180 

            elif event.key == pygame.K_DOWN:
                COORDS[1] -= 5 / (3.1 * SCALE)
                if 2.5 / SCALE > abs(-90 - COORDS[1]):
                    COORDS[1] = -90 + 2.5 / SCALE

            elif event.key == pygame.K_UP:
                COORDS[1] += 5 / (3.1 * SCALE)
                if 2.5 / SCALE > abs(90 - COORDS[1]):
                    COORDS[1] = 90 + 2.5 / SCALE

            map_for_coords(COORDS, SCALE, types[tp])
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 550 <= x <= 600 and 0 <= y <= 50:
                tp += 1
                tp %= 3
            map_for_coords(COORDS, SCALE, types[tp])
    
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), (551, 0, 49, 49))
    pygame.draw.rect(screen, (0, 0, 0), (551, -1, 50, 50), 1)
    screen.blit(Font.render(types[tp], 1, (0, 0, 0)), (556, 14))
    pygame.display.flip()




