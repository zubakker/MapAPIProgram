import pygame
import random
import requests
import sys
import os
from math import pi, tan, atan, e, log, degrees, radians


from map import map_for_coords
from coordinates import get_ll_span
from find import addr_for_coords, org_for_coords


COORDS = [0, 0]
SCALE = 1
zoom = 1

pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = "map.png"

flag = None

Font = pygame.font.SysFont("courier new", 20)
font = pygame.font.SysFont("courier new", 14) 
map_for_coords(COORDS, SCALE,"map", flag)

zooms = { 0.5: 0,
          1: 1,
          2: 2,
          4: 3,
          8: 4,
          16: 5,
          32: 6,
          64: 7,
          128: 8,
          256: 9,
          512: 10,
          1024: 11,
          2048: 12,
          4096: 13,
          8192: 14,
          16384: 15,
          32768: 16,
          65536: 17 }

tp = 0
types = ["map", "skl", "sat"]
adress = ""
full_adr = ""
index = None
mail = 0

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
                zoom += 1
                if zoom > 17:
                    zoom = 17
                if SCALE > 65536:
                    SCALE = 65536
            
            elif event.key == pygame.K_PAGEDOWN:
                SCALE /= 2
#                if 22.5 / SCALE > abs(90 - COORDS[0]) or 22.5 / SCALE > abs(-90 - COORDS[0]) or \
 #                  22.5 / SCALE > abs(180 - COORDS[1]) or 22.5 / SCALE > abs(-180 - COORDS[0]):
  #                  SCALE = max(  22.5 / abs(90 - COORDS[0] - 0.00000001),
   #                               22.5 / abs(-90 - COORDS[0] - 0.00000001),
    #                              22.5 / abs(180 - COORDS[0] - 0.00000001),
     #                             22.5 / abs(-180 - COORDS[0] - 0.00000001) )
                zoom -= 1
                if zoom < 0:
                    zoom = 0
          
            elif event.key == pygame.K_LEFT:
                COORDS[0] -= 45 / (3.1 * SCALE) + 180
                COORDS[0] = COORDS[0] % 360 - 180
            
            elif event.key == pygame.K_RIGHT:
                COORDS[0] += 45 / (3.1 * SCALE) + 180
                COORDS[0] = COORDS[0] % 360 - 180 

            elif event.key == pygame.K_DOWN:
                COORDS[1] -= 45 / (3.1 * SCALE)
                if 22.5 / SCALE > abs(-90 - COORDS[1]):
                    COORDS[1] = -90 + 22.5 / SCALE

            elif event.key == pygame.K_UP:
                COORDS[1] += 45 / (3.1 * SCALE)
                if 22.5 / SCALE > abs(90 - COORDS[1]):
                    COORDS[1] = 90 + 22.5 / SCALE
            
            elif event.key == pygame.K_BACKSPACE and adress and active:
                adress = adress[:-1]
                continue
                
            elif event.key in list(keys) and active:
                adress += keys[event.key]
                continue
            elif event.key == pygame.K_RETURN:
                a, b, c, d = get_ll_span(adress)
                if a:
                    COORDS, SCALE = a, 45 / float(b.split(",")[0])

                    SCALE = int(bin(int(SCALE))[:3] + "0" * ( len(bin(int(SCALE))) - 3 ), 2) * 4
                    zoom = zooms[SCALE]
                    COORDS = [float(COORDS.split(",")[0]), float(COORDS.split(",")[1])]
                    
                    full_adr = c
                    index = d
                    flag = str(COORDS[0]) + "," + str(COORDS[1])
                else:
                    full_adr = "Адрес не найден"

            map_for_coords(COORDS, zoom, types[tp], flag)
        
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
                a, b, c, d = get_ll_span(adress)
                if a:
                    COORDS, SCALE = a, 45 / float(b.split(",")[0])

                    SCALE = int(bin(int(SCALE))[:3] + "0" * ( len(bin(int(SCALE))) - 3 ), 2) * 4
                    zoom = zooms[SCALE]
                    COORDS = [float(COORDS.split(",")[0]), float(COORDS.split(",")[1])]
                    
                    COORDS = [float(COORDS.split(",")[0]), float(COORDS.split(",")[1])]
                    full_adr = c
                    index = d
                else:
                    full_adr = "Адрес не найден"    

            elif 500 <= x <= 550 and 0 <= y <= 50:
                if not flag:
                    flag = get_ll_span(adress)[0]
                elif flag:
                    flag = None

            elif 560 <= x <= 580 and 430 <= y <= 450:
                adress = ""
                full_adr = ""
                flag = None
    
            elif 580 <= x <= 600 and 430 <= y <= 450:
                mail = 1 - mail
                 
            elif event.button == 1 and not active and 45 <= x <= 555:
                Lam = radians(COORDS[0])
                Fi = radians(COORDS[1])

                zx = (256 / (2 * pi)) * (2 ** zoom) * (Lam + pi)
                zy = (256 / (2 * pi)) * (2 ** zoom) * (pi - log( tan(pi/4 + Fi/2), e ) )
                
                x = (zx + x - 300) 
                y = (zy + y - 225) 

                lam = (2 * pi * x) / (256 * 2 ** zoom) - pi
                fi = 2 * atan( e ** ( pi - (2 * pi * y) / (256 * 2 ** zoom) ) ) - pi/2
                
                flag = str(degrees(lam)) + "," + str(degrees(fi))
                a, b = addr_for_coords(flag)
                if a:
                    full_adr = a
                    index = b
        
            elif event.button == 3 and not active and 45 <= x <= 555:
                Lam = radians(COORDS[0])
                Fi = radians(COORDS[1])

                zx = (256 / (2 * pi)) * (2 ** zoom) * (Lam + pi)
                zy = (256 / (2 * pi)) * (2 ** zoom) * (pi - log( tan(pi/4 + Fi/2), e ) )
                
                x = (zx + x - 300) 
                y = (zy + y - 225) 

                lam = (2 * pi * x) / (256 * 2 ** zoom) - pi
                fi = 2 * atan( e ** ( pi - (2 * pi * y) / (256 * 2 ** zoom) ) ) - pi/2
                
                flag = str(degrees(lam)) + "," + str(degrees(fi))
                a = org_for_coords(flag, COORDS)
                full_adr = a


            map_for_coords(COORDS, zoom, types[tp], flag)
    
    screen.blit(pygame.image.load(map_file), (0, 0))

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 44, 450))
    pygame.draw.rect(screen, (0, 0, 0), (556, 0, 44, 450)) 

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
    
    pygame.draw.rect(screen, (255, 255, 255), (0, 430, 560, 20))
    pygame.draw.rect(screen, (0, 0, 0), (-1, 430, 561, 21), 1)
    if index and mail:
        screen.blit(font.render(full_adr + ", " + index, 1, (0, 0, 0)), (558 - font.size(full_adr + ", " + index)[0], 433))
    else:    
        screen.blit(font.render(full_adr, 1, (0, 0, 0)), (558 - font.size(full_adr)[0], 433))
    
    pygame.draw.rect(screen, (255, 255, 255), (560, 430, 20, 20))
    screen.blit(pygame.transform.scale(pygame.image.load("reset.png"), (18, 20)), (560, 430))
    pygame.draw.rect(screen, (0, 0, 0), (559, 430, 21, 21), 1)

    pygame.draw.rect(screen, (255, 255, 255), (580, 430, 20, 20))
    screen.blit(pygame.transform.scale(pygame.image.load("mail.png"), (18, 20)), (580, 430))
    pygame.draw.rect(screen, (0, 0, 0), (579, 430, 21, 21), 1)

    if mail:
        pygame.draw.line(screen, (255, 0, 0), (577, 453), (600, 431), 3)
    
    pygame.display.flip()




