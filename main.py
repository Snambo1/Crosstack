import pygame as pg
import os, sys
print(os.path.dirname(pg.__file__))
from pygame.locals import *

class Platform(pg.sprite.Sprite):
    def __init__(self, x_pos=300, y_pos=300, width=100, height=100, color=(0, 0, 0)):
        super().__init__()
        self.image = pg.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x_pos, y_pos
        self.width, self.height = width, height
        self.color = color

class Player(pg.sprite.Sprite):
    def __init__(self, pos=[75, 75], size=[25, 25]):
        super().__init__()
        self.image = pg.Surface(size)
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos[0], pos[1]
        self.vel = [0, 0]
        self.maxVel = 8

        self.acc = 0.75
        self.width, self.height = size[0], size[1]

    #! Use exponential growth function to model velocity growth.
    #! Use exponential decay function to reset the velocity.
    def move(self, keys, platform):
        dir = [0, 0]
        originalPos = [self.rect.x, self.rect.y]

        # Manage player movement
        if keys[pg.K_SPACE]:
            self.vel[1] = 5

        if keys[pg.K_w]:
            dir[1] = -1
        elif self.vel[1] < 0:
            dir[1] = 1

        if keys[pg.K_a]:
            dir[0] = -1
        elif self.vel[0] < 0:
            dir[0] = 1

        if keys[pg.K_s]:
            dir[1] = 1
        elif self.vel[1] > 0:
            dir[1] = -1

        if keys[pg.K_d]:
            dir[0] = 1
        elif self.vel[0] > 0:
            dir[0] = -1

        newVel = [round(self.vel[0]+self.acc*dir[0], 2), round(self.vel[1]+self.acc*dir[1], 2)]
        if (newVel[0] < self.maxVel and newVel[0] > (-1 * self.maxVel)):
            self.vel[0] = newVel[0]
        if (newVel[1] < self.maxVel and newVel[1] > (-1 * self.maxVel)):
            self.vel[1] = newVel[1]

        # Detect horizontal and vertical collisions
        if self.vel[0]:
            self.rect.x = self.rect.x+self.vel[0]
        if self.vel[1]:
            self.rect.y = self.rect.y+self.vel[1]

        #! Solid rectangle collision detection!
                

pg.init()
clock = pg.time.Clock()

WIN_SIZE = [900, 600]
FPS = 75
win = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption("Crosstack")

player = Player()
platform = Platform()

allSprites = pg.sprite.Group()
allSprites.add(platform, player)

gameRun = True

while gameRun:
    win.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRun = False

    # Get pressed kets
    keys = pg.key.get_pressed()
    player.move(keys, platform)

    if keys[pg.K_q]:
        gameRun = False

    # Draw everything
    allSprites.draw(win)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()