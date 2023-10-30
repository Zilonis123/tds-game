import pygame as pg
import math
import time

from helper.controlls import *
from helper.Visuals.UI import UIe
from helper.Entities.turrets import Turret
from helper.Visuals.renderers import *
from helper.Entities.enemies import Enemy

class SoftwareRenderer():

    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 160*5, 90*5
        self.screen = pg.display.set_mode(self.RES)
        self.FPS = 60
        self.clock = pg.time.Clock()
        
        self.actionRN = "none"

        self.cash = 999 # debug value

        # UI
        # This will be an Array that contains UIe class
        # the type variable lets the code know what turret this is for
        self.UI = [
            UIe(1, (10,5), "blue"),
            UIe(3, (10,125), "green", renderer=triangle_render),
            UIe(4, (10,185), "brown", renderer=hexagon_render),
        ]

        # init turrets
        self.turrets = []
        self.selectedTurret = Turret(1, -999, -999, self)

        self.gridsize=60

        # Enemies
        self.enemies = []


        # bullets
        self.bullets = []

    def draw(self):
        # This func handles anything related to drawing something to the screen
        
        self.screen.fill("darkgray")

        # draw enemies
        for e in self.enemies: e.draw(self)


        # turrets
        self._draw_turrets()

        # bullets
        for b in self.bullets: b.draw(self)

        # draw UI
        self._draw_UI()
    
    def _draw_UI(self):
        bRect = pg.Rect((0,0), (80, self.HEIGHT))
        pg.draw.rect(self.screen, "beige", bRect)
        pg.draw.rect(self.screen, pg.Color(206,126,0), bRect, 4)

        for UIe in self.UI:
            UIe.draw(self)

        # draw grid lines if SHIFT pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            self._draw_grid()
            
    def _draw_grid(self):
        # draw horizonatally
        for i in range(self.WIDTH//self.gridsize+1):
            pg.draw.line(self.screen, "white", (i*self.gridsize, 0), (i*self.gridsize, self.HEIGHT))

        # draw vertically
        for i in range(self.HEIGHT//self.gridsize+1):
            pg.draw.line(self.screen, "white", (0, i*self.gridsize), (self.WIDTH, i*self.gridsize))

    def _draw_turrets(self):

        for turret in self.turrets:
            if self.selectedTurret != "none" and self.selectedTurret == turret:
                continue
            turret.draw(self)

        # draw selected turret 1st
        if self.selectedTurret != "none":
            self.selectedTurret.draw(self)

        
        # draw current in hand
        if self.actionRN == "grabturret":

            # change color depending if the turret can be placed
            rectColor = self.selectedTurret.color
            for turret in self.turrets:
                if turret.plzone.colliderect(self.selectedTurret.rect):
                    rectColor = "red"
                    break

            self.selectedTurret.draw(self, rectColor)

    def handleKeyPress(self):
        pass

    def handleEvents(self):
        # Handles pygame events

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_click(self)

    def run(self):
        # main game loop

        self.running = True
        while self.running:
            self.draw()
            self.handleEvents()
            self.handleKeyPress()

            # Tick enemies
            for enemy in self.enemies:
                enemy.tick(self)

            # Tick bullets
            for bullet in self.bullets:
                bullet.tick(self)

            # tick turrets
            for turret in self.turrets:
                turret.tick(self)

            # Set FPS as the name of the window
            pg.display.set_caption(
                str(math.floor(self.clock.get_fps()))+"FPS - TD")

            keys = pg.key.get_pressed()
            if keys[pg.K_RSHIFT]:
               self.enemies.append(Enemy(1, (200,200)))
            elif keys[pg.K_SPACE]:
                self.enemies = []

            # if turret in hand update self.selectedTurret
            if self.actionRN == "grabturret":
                t = self.selectedTurret.type
                mx,my = pg.mouse.get_pos()
                
                # if grid lines enabled
                if keys[pg.K_LSHIFT]:
                    # snap to grid
                    mx=mx+50/2
                    my=my+50/2
                    mx=round(mx/70)*self.gridsize
                    my=round(my/70)*self.gridsize
                    mx=mx-50-(self.gridsize-50)//2
                    my=my-50-(self.gridsize-50)//2
                else:
                    mx,my = (mx-self.selectedTurret.rect.w//2, my-self.selectedTurret.rect.h//2)
                self.selectedTurret = Turret(t, mx, my, self)

            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":

    start = time.time()
    game = SoftwareRenderer()
    end = time.time()
    print("Took " + str(round(end - start, 2)) + "s to initialize")
    game.run()