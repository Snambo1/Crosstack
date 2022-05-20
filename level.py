import pygame
from tiles import Tile
from settings import tileSize,screenWidth
from player import Player

class level:
    def __init__(self,levelData,surface):
        self.displaySurface=surface
        self.setUpLevel(levelData)
        self.worldShift=0
        self.worldShift2 = 0

    def setUpLevel(self,layout):
        self.tiles=pygame.sprite.Group()
        self.player=pygame.sprite.GroupSingle()
        for rowIndex,row in enumerate(layout):
            for colIndex,col in enumerate(row):
                x = colIndex * tileSize
                y = rowIndex * tileSize
                if col=='X':
                    tile=Tile((x,y),tileSize)
                    self.tiles.add(tile)
                if col=='P':
                    playerSprite = Player((x, y))
                    self.player.add(playerSprite)

    def horizontalMovementCollision(self):
        player =self.player.sprite
        player.rect.x+=player.direction.x*player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x<0:
                    player.rect.left=sprite.rect.right
                elif player.direction.x>0:
                    player.rect.right=sprite.rect.left

    def verticalMovementCollision(self):
        player =self.player.sprite
        player.applyGravity()
        player.rect.y+=player.direction.y*player.speed
        keys = pygame.key.get_pressed()
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y<0:
                    player.rect.top=sprite.rect.bottom
                    player.direction.y = 0
                elif player.direction.y>0:
                    player.rect.bottom=sprite.rect.top
                    player.direction.y = 0

    def run(self):

        self.tiles.update(self.worldShift,self.worldShift2)
        self.tiles.draw(self.displaySurface)

        self.player.update()
        self.horizontalMovementCollision()
        self.verticalMovementCollision()
        self.player.draw(self.displaySurface)
        self.scrollX()

    def scrollX(self):
        player=self.player.sprite
        playerX=player.rect.centerx
        directionX=player.direction.x

        if playerX<screenWidth/4 and directionX<0:
            self.worldShift=8
            player.speed=0
        elif playerX>screenWidth-(screenWidth/4) and directionX>0:
            self.worldShift=-8
            player.speed=0
        else:
            self.worldShift=0
            player.speed=8

    #def scrollY(self):
        #player = self.player.sprite
        #playerY = player.rect.centery
        #directionY = player.direction.y
        #if playerY<screenHeight/4 and directionY<0:
            #self.worldShift2=4
            #player.speed=0
        #elif playerY>screenHeight/4 and directionY>0:
            #self.worldShift2=-2
            #player.speed=0
        #else:
           #self.worldShift2=0
           #player.speed=8
