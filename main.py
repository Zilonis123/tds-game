import pygame as pg
import sys,os,time,math

from src.draw import *
from src.gamestate.run import *
from src.gamestate.draw import *
from src.gamestate.init import change_gamestate
from src.controlls import *
from src.Visuals.UI import UIe
from src.Entities.turrets import Turret
from src.Entities.enemies import Enemy
from src.Entities.Enemies.enemycollisions import check_collisions
from src.waves.wave import Wave
from src.Entities.ttext import Ttext

from loguru import logger 

class SoftwareRenderer():

    def __init__(self):
        pg.init()
        pg.display.set_caption(f"Tower Defense")
        
        self.clearconsole()


        self.RES = self.WIDTH, self.HEIGHT = 160*5, 90*5
        self.screencenter = self.WIDTH//2, self.HEIGHT//2
        self.screen = pg.display.set_mode(self.RES)

        self.FPS = 60
        self.FPSGraph: list[int] = [0 for i in range(200)]

        self.clock = pg.time.Clock()
        
        self.actionRN = None

        self.cash = sys.maxsize # debug value

        self.dir = os.getcwd()

        self.debug = False
        self.speedUp = False # if true game runs 2x faster
        self.gridsize=60

        # init turrets
        self.turrets = []
        self.selectedTurret = None

        
        self.UI = [] 


        # Enemies
        self.enemies: list[Enemy] = []
        self.selectedEnemy: Enemy | None = None
        
        self.wave = 1
        self.currentWave: Wave = Wave(-1)
        self.waveStartedAt = -1 # stores the tick at which the wave started
    

        # bullets
        self.bullets = []

        # self temp text
        self.ttext = []


        self.fonts = {}
        self.imgs = {}

        self.sounds = {}
        self.musicPlaying = None


        self.startTime = time.time()

        self.ticks = 0 # stores the amount of times run() has ran

        self.mousePos: tuple[float, float] = (0,0)
        self.mouseDown: tuple[float, float] = (-99, -99)


        self.gamestate = None
        change_gamestate(self, "Loading")

    def addcash(self, cash):
        def cash_f(self, render):
            self.timeAlive += 1
            self.pos = changeTuple(self.pos, (0, 1))

            if self.timeAlive > 120:
                render.ttext.remove(self)

        clr = "RED" if cash < 0 else "GREEN"
        t = Ttext(str(cash), (self.WIDTH, 50), cash_f, clr, "topright")
        self.ttext.append(t)
        self.cash += cash

    def draw(self):
        # This func handles anything related to drawing something to the screen
        d = {"game": draw_game, "Loading": draw_loading, "mainmenu": draw_mainmenu, "controlls": draw_controlls}

        draw_func = d.get(self.gamestate, None)
        if draw_func != None:
            draw_func(self)


        if self.debug:
            draw_debug(self)


    def handleKeyPress(self):
        mx,my = self.mousePos

        keys = pg.key.get_pressed()
        if keys[pg.K_RSHIFT]:
            self.enemies.append(Enemy("normal", (mx, my)))
            check_collisions(self.enemies[len(self.enemies)-1], self)
        elif keys[pg.K_SPACE]:
            self.enemies = []
        elif keys[pg.K_1]:
            selectTurret(self, 1)
        elif keys[pg.K_2]:
            selectTurret(self, 2)
        elif keys[pg.K_3]:
            selectTurret(self, 3)
        elif keys[pg.K_4]:
            selectTurret(self, 4)

                


    def handleEvents(self):
        # Handles pygame events

        for event in pg.event.get():

            debug = True if pg.key.get_mods() & pg.KMOD_CTRL == 64 else False

            if debug:
                self.debug = not self.debug

            if event.type == pg.QUIT: 
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_down(self)
            elif event.type == pg.MOUSEBUTTONUP:
                mouse_up(self)


            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                if event.mod & pg.KMOD_ALT:
                    self.speedUp = not self.speedUp


    def clearconsole(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def run(self):
        # main game loop

        self.running = True
        while self.running:
            self.ticks += 1

            self.FPSGraph.pop(0)
            self.FPSGraph.append(math.floor(self.clock.get_fps()))

            currentMousePos = pg.mouse.get_pos()
            # check if the mouse moved
            if currentMousePos != self.mousePos:
                mouse_move(self, currentMousePos)
            

            self.draw()
            self.handleKeyPress()
            self.handleEvents()

            d = {"game": run_game, "Loading": run_loading}

            run_f = d.get(self.gamestate, None)
            if run_f != None:
                run_f(self)

            pg.display.flip()
            self.clock.tick(self.FPS)

    def count_entities(self) -> int:
        entities = len(self.turrets) + len(self.bullets) + len(self.enemies)
        return entities

if __name__ == "__main__":

    start = time.time()
    game = SoftwareRenderer()
    end = time.time()
    logger.info("Took " + str(round(end - start, 3)) + "s to initialize")
    game.run()