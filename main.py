import pygame
import os


FPS = 60
WIN_WIDTH = 1000
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
        # Scale object
        if scale != 1:
            self.image = pygame.transform.scale(self.image, (self.rect.width * scale, self.rect.height * scale))
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        WINDOW.blit(self.image, self.rect)


class MoveObject(Sprite):
    def __init__(self, imageName, x, y, scale=1):
        super().__init__(imageName, x, y, scale)
        self.speed = 50

    def moveUp(self):
        self.rect.y -= self.speed / FPS

    def moveDown(self):
        self.rect.y += self.speed / FPS

    def moveLeft(self):
        self.rect.x -= self.speed / FPS

    def moveRight(self):
        self.rect.x += self.speed / FPS

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

pygame.init()
# for i, onj in enumerate(enemies.children):
#     ...
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Objects init
mainTank = MainObject('tank.png', WIN_WIDTH/2, 100, 5)

tank02 = MoveObject('tank01.png', 300, 0, 5)

while GAME_RUN:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            GAME_RUN = False

    # Logik
    mainTank.control()
    tank02.control()
    # Draw
    WINDOW.fill(COLOR_FIELD)
    mainTank.update()
    tank02.update()

    pygame.display.update()
    clock.tick()