import pygame, sys
from settings import *
from level import level


pygame.init()
screen=pygame.display.set_mode((screenWidth,screenHeight))
clock=pygame.time.Clock()
level=level(levelMap,screen)
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('white')
    level.run()

    pygame.display.update()
    clock.tick(60)
