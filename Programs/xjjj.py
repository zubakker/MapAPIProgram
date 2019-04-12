import pygame
import random
import requests
import sys
import os


from map import map_for_coords
from coordinates import get_ll_span


COORDS = 0, 0
SCALE = 1.0

pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = "map.png"

flag = None

Font = pygame.font.SysFont("courier new", 20)
map_for_coords(COORDS, SCALE,"map", flag)

tp = 0
types = ["map", "skl", "sat"]
adress = ""

keys = {102: "а", 44: "б", 100: "в", 117: "г", 48: "0", 54: "6",
        108: "д", 116: "е", 96: "ё", 59: "ж", 49: "1", 55: "7",
        112: "з", 98: "и", 113: "й", 114: "к", 50: "2", 56: "8",
        107: "л", 118: "м", 121: "н", 106: "о", 51: "3", 57: "9",
        103: "п", 104: "р", 99: "с", 110: "т", 52: "4", 45: "-",
        101: "у", 97: "ф", 91: "х", 119: "ц", 53: "5",
        120: "ч", 105: "ш", 111: "щ", 93: "ъ", 32: " ",
        115: "ы", 109: "ь", 39: "э", 46: "ю", 122: "я"}
active = False
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
            
            elif event.key == pygame.K_BACKSPACE and adress and active:
                adress = adress[:-1]
                continue
                
            elif event.key in list(keys) and active:
                adress += keys[event.key]
                continue
            elif event.key == pygame.K_RETURN:
                a, b = get_ll_span(adress)
                if a:
                    COORDS, SCALE = a, 5 / float(b.split(",")[0])
                    COORDS = [float(COORDS.split(",")[0]), float(COORDS.split(",")[1])]

            map_for_coords(COORDS, SCALE, types[tp], flag)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if not (0 <= x <= 450 and 0 <= y <= 50):
                active = False
            else:
                active = True

            if 550 <= x <= 600 and 0 <= y <= 50:
                tp += 1
                tp %= 3
            elif 450 <= x <= 500 and 0 <= y <= 50:
                a, b = get_ll_span(adress)
                if a:
                    COORDS, SCALE = a, 5 / float(b.split(",")[0])
                    COORDS = [float(COORDS.split(",")[0]), float(COORDS.split(",")[1])]
            
            elif 500 <= x <= 550 and 0 <= y <= 50:
                if not flag:
                    flag = get_ll_span(adress)[0]
                elif flag:
                    flag = None
            map_for_coords(COORDS, SCALE, types[tp], flag)
    
    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.draw.rect(screen, (255, 255, 255), (550, 0, 50, 49))
    pygame.draw.rect(screen, (0, 0, 0), (550, -1, 50, 50), 1)
    screen.blit(Font.render(types[tp], 1, (0, 0, 0)), (556, 14))

    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 451, 49))
    pygame.draw.rect(screen, (0, 0, 0,), (-1, -1, 453, 50), 1)
    screen.blit(Font.render(adress, 1, (0, 0, 0)), (450 - Font.size(adress)[0], 16))

    pygame.draw.rect(screen, (255, 255, 255), (450, 0, 50, 49))
    pygame.draw.rect(screen, (0, 0, 0), (450, -1, 51, 50), 1)
    screen.blit(pygame.transform.scale(pygame.image.load("glass.png"), (45, 45)), (452, 2))    
    
    pygame.draw.rect(screen, (255, 255, 255), (501, 0, 50, 49))
    pygame.draw.rect(screen, (0, 0, 0), (500, -1, 51, 50), 1)
    screen.blit(pygame.transform.scale(pygame.image.load("flag.png"), (45, 45)), (502, 2))    
    if flag:
        pygame.draw.line(screen, (255, 0, 0), (503, 47), (547, 0), 5)
    
    pygame.display.flip()




