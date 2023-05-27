import pygame
import os
from map import *


def draw_map():
    for y in range(len(map_data)):
        for x in range(len(map_data[y])):
            blockg = map_data[y][x]
            if blockg == 1:
                blocks.append(Block('brick.png', x * block_size, y * block_size, 5))
            if blockg == 2:
                tanks.append(MainObject('tank.png', x * block_size, y * block_size, 4.7))
            if blockg == 3:
                tanks.append(AIObject('tank01.png', x * block_size, y * block_size, 5))
                

FPS = 60
WIN_WIDTH = 1680
WIN_HEIGHT = 800

PATH = os.path.dirname(__file__) + os.sep
PATH_IMG = PATH + 'images' + os.sep

GAME_RUN = True

COLOR_FIELD = (150, 0, 50)

clock = pygame.time.Clock()

class Sprite(pygame.sprite.Sprite):
    def __init__(self, imageName, x, y,  scale=1):
        self.image = pygame.image.load(PATH_IMG + imageName)
        self.rect = self.image.get_rect()
        self.direction = "up"
        # Scale object
        if scale != 1:
            self.image = pygame.transform.scale(self.image, (self.rect.width * scale, self.rect.height * scale))
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.direction == "left":
            WINDOW.blit(pygame.transform.rotate(self.image, 90), self.rect)
        elif self.direction == "right":
            WINDOW.blit(pygame.transform.rotate(self.image, -90), self.rect)
        elif self.direction == "up":
            WINDOW.blit(self.image, self.rect)
        elif self.direction == "down":
           WINDOW.blit(pygame.transform.flip(self.image, False, True), self.rect)


class MoveObject(Sprite):
    def __init__(self, imageName, x, y, scale=1):
        super().__init__(imageName, x, y, scale)
        self.speed = 50
        

    def moveUp(self):
        self.rect.y -= self.speed / FPS
        self.direction = "up"

    def moveDown(self):
        self.rect.y += self.speed / FPS
        self.direction = "down"    
    def moveLeft(self):
        self.rect.x -= self.speed / FPS
        self.direction = "left"

    def moveRight(self):
        self.rect.x += self.speed / FPS
        self.direction = "right"

    def control(self):
        ...

MOVE_RIGHT = 1
MOVE_LEFT = 0
class AIObject(MoveObject):
    direction = MOVE_RIGHT
    def control(self):
        if self.rect.right >= WIN_WIDTH:
            self.direction = MOVE_LEFT
        if self.rect.x < 0:
            self.direction = MOVE_RIGHT

        if self.direction == MOVE_RIGHT:
            self.moveRight()
        if self.direction == MOVE_LEFT:
            self.moveLeft()

class MainObject(MoveObject):
    def control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.moveUp()
        if keys[pygame.K_s]:
            self.moveDown()
        if keys[pygame.K_a]:
            self.moveLeft()
        if keys[pygame.K_d]:
            self.moveRight()
class Block(Sprite):
    def checkCollision(self, anotherOBJ):
        return self.rect.colliderect(anotherOBJ)
        



pygame.init()
# for i, onj in enumerate(enemies.children):
#     ...
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

font = pygame.font.Font(None, 36)

# Objects init
tanks = []
blocks = []
draw_map()
while GAME_RUN:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            GAME_RUN = False

    # Logik
    for tank in tanks:
        tank.control()
    
    for tank in tanks:
        for block in blocks:
            
            if block.checkCollision(tank):
                dx = tank.rect.x - block.rect.x
                dy = tank.rect.y - block.rect.y

                if abs(dx) > abs(dy):
                    if dx > 0:
                        tank.rect.x = block.rect.x + block.rect.width
                    else:
                        tank.rect.x = block.rect.x - block.rect.width
                else:
                    if dy > 0:
                        tank.rect.y = block.rect.y + block.rect.height
                    else:
                        tank.rect.y = block.rect.y - block.rect.height
    # Draw
    WINDOW.fill(COLOR_FIELD)
    text = font.render("Laser Tanks! Alpha 0.1.2.1", True, (0, 255, 0))
    text2 = font.render("Change Log: Added Map, Collision, Move Direction", True, (0, 255, 0))
    WINDOW.blit(text, (WIN_WIDTH - text.get_width(),0))
    WINDOW.blit(text2, (WIN_WIDTH - text2.get_width(),20))
    for tank in tanks:
        tank.update()
        
    for block6 in blocks:
        block6.update()
    

    pygame.display.update()
    clock.tick()