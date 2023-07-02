import asyncio
import time

import pygame as pg
from scripts.DrawRectAlpha import draw_rect_alpha
from scripts.Smooth import exponential_decay_smoothing
#sounds
pg.mixer.init()
shootSound = pg.mixer.Sound("..\\sounds\\shoot1.wav")

WINDOW = None
camerapos = {'x':0, 'y':0}
FPS = 60
anims = []

def INIT(window,campos,animg):
    global WINDOW, anims, camerapos
    anims = animg
    camerapos = campos
    WINDOW = window

class Object:

    def __init__(self, w=10, h=10, x=0, y=0, color=(0, 0, 0, 0), window_inst=None, transperent=0):
        self.tag = "obj"
        self.args = [x, y, w, h, color, window_inst, transperent]
        self.resolution = pg.display.get_window_size()
        self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])
        self.count = -1
    def update(self):
        draw_rect_alpha(self.args[5], self.args[4], self.rect)
        if(self.count>=0):
            print(self.count)
            self.count+=1


class EndTrigger:

    def __init__(self, w=10, h=10, x=0, y=0, window_inst=None, transperent=0):
        self.tag = "endtrg"
        self.args = [x, y, w, h, window_inst, transperent]
        self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])

    def update(self):
        try:
            self.args[0] -= 6
            self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])
        except:
            print("ERROR: SOMETHING GOT WRONG: " + Exception.__name__)
class QTEObject:

    def __init__(self, w=10, h=10, x=0, y=0, color=(0, 0, 0), window_inst=None, transperent=0):
        self.tag = "qteobj"
        self.args = [x, y, w, h, color, window_inst, transperent]
        self.resolution = pg.display.get_window_size()
        self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])

    def update(self):
        try:
            draw_rect_alpha(self.args[5], self.args[4], self.rect)
            self.args[0] -= 6
            self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])
        except:
            print("ERROR: SOMETHING GOT WRONG: " + Exception.__name__)

class PlayerControl:

    def __init__(self, colliders=None, w=10, h=10, x=0, y=0, color=(0, 0, 0), window_inst=None, transperent=0):
        self.tag = "plr"
        self.args = [x, y, w, h, color, window_inst, transperent]
        self.resolution = pg.display.get_window_size()
        self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])
        self.colliders = colliders

    def update(self):
        try:
            draw_rect_alpha(self.args[5], self.args[4], self.rect)
            return self.Collider()
        except:
            print("ERROR: SOMETHING GOT WRONG")

    def Collider(self):
        for collider in self.colliders:
            if collider.rect.colliderect(self.rect):
                if collider.tag == "qteobj":
                    pgKey = pg.key.get_pressed()
                    if pgKey[pg.K_e]:
                        return collider.rect
                    else:
                        return "failed"
                elif collider.tag == "endtrg":
                    return "shouldEnd"
class Image:

    def __init__(self, scale=1, x=0, y=0, color=(0, 0, 0), window_inst=None, image=None, scalex=100, scaley=100):
        self.tag = "obj"
        self.scale = scale
        self.image = pg.image.load(image).convert_alpha()
        self.args = [x, y, scalex, scaley, color, window_inst]
        self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])
        self.image=pg.transform.scale(self.image, (self.args[2], self.args[3]))

    def update(self):
        self.image=pg.transform.scale(self.image, (self.args[2], self.args[3]))
        self.args[5].blit(self.image, (self.rect.x, self.rect.y))


class TextObject:
    def __init__(self, text="NULL", fontSize=10, x=0, y=0, color=(0, 0, 0), window_inst=None, functionalTag="NONE"):
        self.tag = "txt"
        self.functionalTag = functionalTag
        self.args = [x, y, color, window_inst, text]
        self.font = pg.font.SysFont('chalkduster.ttf', fontSize)
        self.text = self.font.render(text, True, color)

    def update(self):
        self.text = self.font.render(self.args[4], True, self.args[2])
        self.args[3].blit(self.text, (
        self.args[0] - self.text.get_rect().width / 2, self.args[1] - self.text.get_rect().height / 2))


class Button:
    def __init__(self, w=10, h=10, x=0, y=0, color=(0, 0, 0), window_inst=None, colortext=(100, 100, 0), fontSize=20,
                 text="NULL", funcs="none"):
        self.funcs = funcs
        self.tag = "btn"
        self.args = [x, y, w, h, window_inst]
        self.color = color
        self.font = pg.font.SysFont('chalkduster.ttf', fontSize)
        self.text = self.font.render(text, True, colortext)
        self.rect = pg.Rect(self.args[0], self.args[1], self.args[2], self.args[3])
        self.colordef = color

    def update(self):
        try:
            pg.draw.rect(self.args[4], self.color, self.rect, 0, border_radius=10)
            self.args[4].blit(self.text, (self.rect.centerx - self.text.get_rect().width / 2, self.rect.centery))

            if self.rect.collidepoint(pg.mouse.get_pos()):
                self.color = (255, 255, 255)
            else:
                self.color = self.colordef
        except:
            print("ERROR: SOMETHING GOT WRONG: " + Exception.__name__)


class Sprite(pg.sprite.Sprite):
    def __init__(self, imageName, x, y, scale=1, type="none"):
        self.image = pg.image.load("..\\sprites\\" + imageName)
        self.rect = self.image.get_rect()
        self.direction = "up"
        self.type = type
        self.scale = scale
        # Scale object
        if self.scale != 1:
            self.image = pg.transform.scale(self.image,
                                                (self.rect.width * self.scale, self.rect.height * self.scale))
            self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def changeImage(self, newImage):
        self.image = pg.image.load("..\\sprites\\" + newImage)
        # self.rect = self.image.get_rect()
        if self.scale != 1:
            self.image = pg.transform.scale(self.image, (self.rect.width, self.rect.height))

    def update(self):
        if self.direction == "left":
            WINDOW.blit(pg.transform.rotate(self.image, 90),
                        (self.rect.x - camerapos["x"], self.rect.y - camerapos["y"]))
        elif self.direction == "right":
            WINDOW.blit(pg.transform.rotate(self.image, -90),
                        (self.rect.x - camerapos["x"], self.rect.y - camerapos["y"]))
        elif self.direction == "up":
            WINDOW.blit(self.image, (self.rect.x - camerapos["x"], self.rect.y - camerapos["y"]))
        elif self.direction == "down":
            WINDOW.blit(pg.transform.rotate(self.image, -180),
                        (self.rect.x - camerapos["x"], self.rect.y - camerapos["y"]))


class MoveObject(Sprite):
    def __init__(self, imageName, x, y, scale=1, type="none", name="tankplr"):
        super().__init__(imageName, x, y, scale)
        self.speed = 50
        self.type = type
        self.name = name

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
    def __init__(self, imageName, x, y, scale=1, type="none", name="tankplr"):
        super().__init__(imageName, x, y, scale, type, name)
        self.name = "enemy"
        self.rays = []

    direction = MOVE_RIGHT


    def update(self):

        return super().update()


class MainObject(MoveObject):
    def __init__(self, imageName, x, y, scale=1, type="none"):
        super().__init__(imageName, x, y, scale, type)
        self.dely = 0
        self.type = "plr"
        self.projectiles = []

    def control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.moveUp()
        if keys[pg.K_s]:
            self.moveDown()
        if keys[pg.K_a]:
            self.moveLeft()
        if keys[pg.K_d]:
            self.moveRight()
        if keys[pg.K_e]:

            if self.dely >= 40:
                anims[0].Play()
                self.dely = 0
                self.projectiles.append(ProjectileController("laseranim1.png",
                                                        self.rect.x,
                                                        self.rect.y,
                                                        4.7,
                                                        "projectile",
                                                        self.direction,
                                                        "tankplr"
                                                        ))
                pg.mixer.Sound.play(shootSound)
                pg.mixer.music.stop()

                print(self.projectiles)


    def update(self):
        self.dely += 1

        return super().update()


class Block(Sprite):
    def checkCollision(self, anotherOBJ):
        return self.rect.colliderect(anotherOBJ)


class ProjectileController(Sprite):
    def __init__(self, imageName, x, y, scale=1, type="none", dir="up", parent="none"):
        super().__init__(imageName, x, y, scale, type)
        self.direction = dir
        self.parent = parent

    def update(self):
        if (self.direction == "left"):
            self.rect.x -= 30
        if (self.direction == "up"):
            self.rect.y -= 30
        if (self.direction == "right"):
            self.rect.x += 30
        if (self.direction == "down"):
            self.rect.y += 30
        return super().update()

    def checkCollision(self, obj):
        if (obj.name != self.parent):
            return self.rect.colliderect(obj.rect)
