import pygame as pg
from pygame.locals import *

pg.init()
clock = pg.time.Clock()

WIN_SIZE = [900, 600]
FPS = 60
win = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption("Crosstack")

gameRun = True

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
        self.maxVel = 6
        self.inAir = True

        self.acc = 1
        self.width, self.height = size[0], size[1]

    #! Use exponential growth function to model velocity growth.
    #! Use exponential decay function to reset the velocity.
    def updatePlayer(self, keys, platforms):
        dir = [0, 0]

        # Manage player movement
        if keys[pg.K_a]:
            dir[0] = -1
        elif self.vel[0] < 0:
            dir[0] = 1

        if keys[pg.K_s]:
            dir[1] = 1

        if keys[pg.K_d]:
            dir[0] = 1
        elif self.vel[0] > 0:
            dir[0] = -1

        if keys[pg.K_SPACE]:
            if not self.inAir:
                self.vel[1] = -16
                self.inAir = True

        if self.vel[1] < 12:
            self.vel[1]+=self.acc

        newVel = [round(self.vel[0]+self.acc*dir[0], 2), round(self.vel[1]+self.acc*dir[1], 2)]
        if (abs(newVel[0]) <= self.maxVel):
            self.vel[0] = newVel[0]
        if (abs(newVel[1]) <= self.maxVel):
            self.vel[1] = newVel[1]

        if abs(self.vel[0]):
            self.rect.x+=self.vel[0]
            for platform in platforms:
                if pg.Rect.colliderect(self.rect, platform.rect):
                    if self.rect.left < platform.rect.left:
                        self.rect.x = platform.rect.left-self.width
                    else:
                        self.rect.x = platform.rect.right

        if abs(self.vel[1]):
            self.rect.y+=self.vel[1]
            platform = pg.sprite.spritecollideany(self, platforms)
            if platform != None:
                if self.rect.top < platform.rect.top:
                    self.rect.y = platform.rect.top-self.height
                    self.inAir = False
                else:
                    self.rect.y = platform.rect.bottom
                    self.vel[1] = 0

        win.blit(self.image, (self.rect.x, self.rect.y))

player = Player()

ground = Platform(x_pos=0, y_pos=WIN_SIZE[1]-25, width=WIN_SIZE[0], height=25)
platform1 = Platform(x_pos=50, y_pos=190, width=100, height=25, color=(0, 155, 0))
platform2 = Platform(x_pos=150, y_pos=280, width=100, height=25, color=(0, 155, 0))
platform3 = Platform(x_pos=250, y_pos=370, width=100, height=25, color=(0, 155, 0))
platform4 = Platform(x_pos=350, y_pos=460, width=100, height=25, color=(0, 155, 0))
platform5 = Platform(x_pos=450, y_pos=550, width=100, height=25, color=(0, 155, 0))

platforms = pg.sprite.Group()
platforms.add(ground, platform1, platform2, platform3, platform4, platform5)

while gameRun:
    win.fill((255, 255, 255))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            gameRun = False

    # Get pressed kets
    keys = pg.key.get_pressed()

    player.updatePlayer(keys, platforms)

    if keys[pg.K_q]:
        gameRun = False

    # Draw platforms
    platforms.draw(win)

    pg.display.flip()
    clock.tick(FPS)

pg.quit()