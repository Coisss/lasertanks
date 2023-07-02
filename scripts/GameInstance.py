import pygame as pg
from scripts.GameObjects import * # Підключає всі об'єкти з файлу GameObjects.py, треба для відображення об'єктів
from scripts.MapSet import * # Підключає всі змінні з файлу MapSet.pу, для роботи з рівнями.
from scripts.AnimationControl import AnimationController
from scripts.Smooth import exponential_decay_smoothing


class GameInstance:
    def __init__(self, res=(700, 700)):
        pg.init()
        self.key = pg.K_e
        self.WINDOW = pg.display.set_mode(res) # Ініціалізує вікно
        pg.display.set_caption("Laser Tanks!")
        self.FPS = 60 # Змінна яка визначає, скільки буде кадрів в секунду
        self.CLOCK = pg.time.Clock() # Змінна, для оновлення екрану
        self.menu = MainMenu(window=self.WINDOW, clock=self.CLOCK) # Ініціалізування головного меню
        self.levelselect = LevelSelect(window=self.WINDOW, clock=self.CLOCK)  # Ініціалізування головного меню
        self.options = Options(window=self.WINDOW, clock=self.CLOCK) # Ініціалізування Опцій
        self.level1 = Game(window=self.WINDOW, clock=self.CLOCK, level=level1) # Ініціалізування першого рівня
        self.level2 = Game(window=self.WINDOW, clock=self.CLOCK, level=level2)  # Ініціалізування другого рівня
        self.level3 = Game(window=self.WINDOW, clock=self.CLOCK, level=level3)  # Ініціалізування третього рівня
        self.level4 = Game(window=self.WINDOW, clock=self.CLOCK, level=level4)  # Ініціалізування четвертого рівня
        self.level5 = Game(window=self.WINDOW, clock=self.CLOCK, level=level5)  # Ініціалізування п'ятого рівня
        self.currentInstance = self.menu # Призначаєм меню як початкову сцену
        self.UpdateApp() # Викликаємо функцію оновлення гри




    def ChangeInstance(self, instance): # Функція для зміни сцени гри
        self.currentInstance = instance # Призначаємо змінну instance як поточну сцену
        self.currentInstance.LoadInstance() # Підвантажуємо об'єкти з зміненої сцени
    def UpdateApp(self): # Функція оновлення гри
        while True: # Оголошуємо цикл для роботи зі сценами
            result = self.currentInstance.UpdateElements() # Призначаємо змінній result, значення з функції оновлення сцени (приклад: result = "stop")
            if result == "stop": # Якщо result дорівнює "stop" то
                print("succesfully stopped current Instance.") # Виводимо що гра закрилась
                break # Виходимо з циклу, тим самим закриваємо гру
            elif result == "options": # Якщо ж result дорівнює "options" то
                print("switched frame - to options.") # виводимо про зміну сцени на опції
                self.ChangeInstance(self.options) # змінюємо сцену на опції
            elif result == "levelSelect": # А якщо result дорівнює "mainMenu" то
                print("switched frame - to levelSelect.") # виводимо про зміну поточної сцени на головне меню
                self.ChangeInstance(self.levelselect) # змінюємо поточну сцену на головне меню
            elif result == "mainMenu": # А якщо result дорівнює "mainMenu" то
                print("switched frame - to mainMenu.") # виводимо про зміну поточної сцени на головне меню
                self.ChangeInstance(self.menu) # змінюємо поточну сцену на головне меню
            elif result == "level1": # І якщо result дорівнює "level1" то
                print("switched frame - to Level 1.") # Повідомляємо про зміну поточної сцени на Level 1
                self.ChangeInstance(self.level1) # змінюємо сцену на Level 1
            elif result == "level2": # І якщо result дорівнює "level2" то
                print("switched frame - to Level 2.") # Повідомляємо про зміну поточної сцени на Level 2
                self.ChangeInstance(self.level2) # змінюємо сцену на Level 2
            elif result == "level3": # І якщо result дорівнює "level3" то
                print("switched frame - to Level 3.") # Повідомляємо про зміну поточної сцени на Level 3
                self.ChangeInstance(self.level3) # змінюємо сцену на Level 3
            elif result == "level4": # І якщо result дорівнює "level4" то
                print("switched frame - to Level 4.") # Повідомляємо про зміну поточної сцени на Level 4
                self.ChangeInstance(self.level4) # змінюємо сцену на Level 4
            elif result == "level5": # І якщо result дорівнює "level5" то
                print("switched frame - to Level 5.") # Повідомляємо про зміну поточної сцени на Level 5
                self.ChangeInstance(self.level5) # змінюємо сцену на Level 5

class Options:
    def __init__(self, window: pg.Surface, clock: pg.time.Clock): # Ініціалізуємо змінні для роботи сцени Опції
        self.WINDOW = window
        self.key = "E"
        self.resolution = (window.get_width(), window.get_height())
        self.SceneObjects = []
        self.LoadInstance()
        self.clock = clock
    def LoadInstance(self): # Завантажуємо у пам'ять об'єкти сцени

        self.SceneObjects.append(Object(w=500,x=self.resolution[0]/2 - 500/2, h=self.resolution[1], color=(0, 0, 15,150), window_inst=self.WINDOW))

        self.SceneObjects.append(
            TextObject(fontSize=72, text="OPTIONS", x=self.resolution[0] / 2, y=self.resolution[1] / 3,
                       color=(15, 150, 255), window_inst=self.WINDOW)) # Заголовок
        self.SceneObjects.append(
            TextObject(fontSize=32, text="MAIN OPTIONS OF THE GAME.", x=self.resolution[0] / 2, y=self.resolution[1] / 3 + 50,
                       color=(255, 255, 15), window_inst=self.WINDOW)) # Підзаголовок
        self.SceneObjects.append(
            TextObject(fontSize=32, text="Shoot key is: \"E\"", x=self.resolution[0] / 2, y=self.resolution[1] / 2 + 60,
                       color=(255, 255, 15), window_inst=self.WINDOW,functionalTag="CurrentKey")) # Яка клавіша для керування
        self.SceneObjects.append(
            TextObject(fontSize=32, text="ESC - to return to main menu", x=self.resolution[0] / 2, y=self.resolution[1] / 2 + 100,
                       color=(255, 255, 15), window_inst=self.WINDOW,functionalTag="CurrentKeyToMainMenu")) # Яка клавіша для керування
        self.SceneObjects.append(
            TextObject(fontSize=32, text="(Working only in Game)", x=self.resolution[0] / 2, y=self.resolution[1] / 2 + 120,
                       color=(255, 255, 15), window_inst=self.WINDOW,functionalTag="CurrentKeyToMainMenu2")) # Яка клавіша для керування
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="BACK", fontSize=30, y=self.resolution[1] / 3 + 310, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="mainMenu")) # кнопка до головного меню
    def UpdateElements(self): # Функція оновлення
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "stop"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                for Object in self.SceneObjects:
                    if Object.tag == "btn":
                        if Object.rect.collidepoint(pos):
                            if Object.funcs == "mainMenu":
                                return "mainMenu"
        self.WINDOW.fill("gray")
        for Object in self.SceneObjects:
            Object.update()
        pg.display.flip()

        self.clock.tick(60)

class LevelSelect:
    def __init__(self, window: pg.Surface, clock: pg.time.Clock):
        self.WINDOW = window
        self.resolution = (window.get_width(), window.get_height())
        self.SceneObjects = []
        self.LoadInstance()
        self.clock = clock
    def LoadInstance(self):
        self.WINDOW.fill("gray")
        self.SceneObjects.append(Object(w=600,x=self.resolution[0]/2 - 600/2, h=self.resolution[1], color=(0, 0, 15,150), window_inst=self.WINDOW))

        self.SceneObjects.append(
            TextObject(fontSize=72, text="Level select screen", x=self.resolution[0] / 2, y=self.resolution[1] / 3,
                       color=(15, 150, 255), window_inst=self.WINDOW))
        self.SceneObjects.append(
            TextObject(fontSize=32, text="Select level, to play it!", x=self.resolution[0] / 2, y=self.resolution[1] / 3 + 50,
                       color=(255, 255, 15), window_inst=self.WINDOW))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2 -200/2, text="Level 1", fontSize=30, y=self.resolution[1] / 3 + 90, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="level1"))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="Level 2", fontSize=30, y=self.resolution[1] / 3 + 180, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="level2"))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="Level 3", fontSize=30, y=self.resolution[1] / 3 + 270, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="level3"))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="Level 4", fontSize=30, y=self.resolution[1] / 3 + 360, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="level4"))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="Level 5", fontSize=30, y=self.resolution[1] / 3 + 450, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="level5"))

        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="Back", fontSize=30, y=self.resolution[1] / 3 + 520, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="back"))
    def UpdateElements(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "stop"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                for Object in self.SceneObjects:
                    if Object.tag == "btn":
                        if Object.rect.collidepoint(pos):
                            if Object.funcs != "back":
                                return Object.funcs
                            else:
                                return "mainMenu"


        for Object in self.SceneObjects:
            Object.update()

        pg.display.flip()

        self.clock.tick(60)

        return "update"

class MainMenu:
    def __init__(self, window: pg.Surface, clock: pg.time.Clock):
        self.WINDOW = window
        self.resolution = (window.get_width(), window.get_height())
        self.SceneObjects = []
        self.LoadInstance()
        self.clock = clock
    def LoadInstance(self):
        self.WINDOW.fill("gray")
        self.SceneObjects.append(Object(w=600,x=self.resolution[0]/2 - 600/2, h=self.resolution[1], color=(0, 0, 15,150), window_inst=self.WINDOW))

        self.SceneObjects.append(
            TextObject(fontSize=72, text="Laser Tanks!", x=self.resolution[0] / 2, y=self.resolution[1] / 3,
                       color=(15, 150, 255), window_inst=self.WINDOW))
        self.SceneObjects.append(
            TextObject(fontSize=32, text="Game made on pygame. Currently has 5 level avaible.", x=self.resolution[0] / 2, y=self.resolution[1] / 3 + 50,
                       color=(255, 255, 15), window_inst=self.WINDOW))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2 -200/2, text="Play", fontSize=30, y=self.resolution[1] / 3 + 130, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="runTheGame"))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="Options", fontSize=30, y=self.resolution[1] / 3 + 210, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="options"))
        self.SceneObjects.append(
            Button(w=200, x=self.resolution[0] / 2-200/2, text="Quit", fontSize=30, y=self.resolution[1] / 3 + 310, h=50,
                   color=(0, 0, 15), window_inst=self.WINDOW, funcs="terminateApp"))
    def UpdateElements(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "stop"
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                for Object in self.SceneObjects:
                    if Object.tag == "btn":
                        if Object.rect.collidepoint(pos):
                            if Object.funcs == "options":
                                return "options"
                            elif Object.funcs == "terminateApp":
                                return "stop"
                            elif Object.funcs == "runTheGame":
                                return "levelSelect"

        for Object in self.SceneObjects:
            Object.update()

        pg.display.flip()

        self.clock.tick(60)

        return "update"
class Game:
    def __init__(self, window: pg.Surface, clock: pg.time.Clock, level):
        self.WINDOW = window
        self.resolution = (window.get_width(), window.get_height())
        self.SceneObjects = []
        self.GameObjects = []
        self.Characters = {}
        self.tanks = {}
        self.Keys = []
        self.levelMapSet = level
        self.clock = clock
        self.anims = []
        self.score=0
        self.camerapos = {'x':0,'y':0}
        self.prevvalx = 0
        self.prevvaly = 0
        self.missed=0
        self.blocks = []
        self.projectiles = []
        self.animSeqPlr = ["tankshoot1.png", "tankshoot2.png", "tank.png"]
        self.LoadInstance()


    def LoadInstance(self):
        enemyCounter = 0
        for y in range(len(self.levelMapSet)):
            for x in range(len(self.levelMapSet[y])):
                enemyCounter += 1
                blockg = self.levelMapSet[y][x]
                if blockg == 1:
                    self.blocks.append(Block('brick.png', x * 5 *22, y * 5 *22, 5, type="block"))
                if blockg == 2:
                    self.tanks['plr'] = MainObject('tank.png', x * 5 *22, y * 5 *22, 4.7, type="player")
                if blockg == 3:
                    self.tanks['enemies' + str(enemyCounter)] = AIObject('tank01.png', x * 5 *22, y * 5 *22, 5,
                                                                    type="enemy")


        self.anims.append(AnimationController(animSeq=self.animSeqPlr, delaybtwFrames=10, sprite=self.tanks['plr'], loop=False, flip=False))
        self.SceneObjects.append(
            TextObject(fontSize=72, text="SCORE: ", x=self.resolution[0] / 2, y=20,
                       color=(15, 150, 255), window_inst=self.WINDOW))
    def UpdateElements(self):
        INIT(self.WINDOW,self.camerapos,self.anims)
        self.WINDOW.fill("gray")
        for i in range(25):
            self.camerapos = {'x': exponential_decay_smoothing(self.prevvalx, self.tanks['plr'].rect.x - 700 / 2 + self.tanks[
                'plr'].rect.width / 2, 0.0005),
                         'y': exponential_decay_smoothing(self.prevvaly, self.tanks['plr'].rect.y - 700 / 2 + self.tanks[
                             'plr'].rect.height / 2, 0.0005)}

            self.prevvaly = self.camerapos['y']
            self.prevvalx = self.camerapos['x']
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                return "stop"

        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            return "mainMenu"
        # collision
        try:
            for tank in self.tanks:
                for block in self.blocks:
                    if block.checkCollision(self.tanks[tank]):
                        dx = self.tanks[tank].rect.x - block.rect.x
                        dy = self.tanks[tank].rect.y - block.rect.y

                        if abs(dx) > abs(dy):
                            if dx > 0:
                                self.tanks[tank].rect.x = block.rect.x + block.rect.width
                            else:
                                self.tanks[tank].rect.x = block.rect.x - block.rect.width
                        else:
                            if dy > 0:
                                self.tanks[tank].rect.y = block.rect.y + block.rect.height
                            else:
                                self.tanks[tank].rect.y = block.rect.y - block.rect.height
        except:
            ...
        try:
            for block in self.blocks:
                for proj in self.projectiles:
                    if block.checkCollision(proj):
                        self.projectiles.remove(proj)
        except: ...
        # Draw
        try:
            for tank in self.tanks:
                self.tanks[tank].update()
                self.tanks[tank].control()
                if(self.tanks[tank].type =="plr"):
                    self.projectiles = self.tanks[tank].projectiles
        except:
            ...
        for block6 in self.blocks:
            block6.update()
        try:
            for projectile in self.projectiles:
                projectile.update()
                try:
                    for tank in self.tanks:
                        if projectile.checkCollision(self.tanks[tank]):
                            self.tanks.pop(tank)
                            self.score += 10
                            self.projectiles.remove(projectile)
                except:
                    ...
        except: ...
        for anim in self.anims:
            anim.Update()
        for object in self.SceneObjects:
            object.update()
            object.args[0] = object.text.get_rect().width / 2
            object.args[4] = "SCORE: " + str(self.score)

        pg.display.update()
        self.clock.tick()

        return "update"
