import pygame as pg
import math

from helper.controlls import *
from helper.UI import UIe
from helper.turrets import Turret
from helper.renderers import *
from helper.enemies import Enemy

class SoftwareRenderer():

    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 160*5, 90*5
        self.screen = pg.display.set_mode(self.RES)
        self.FPS = 60
        self.clock = pg.time.Clock()
        
        self.actionRN = "none"


        # UI
        # This will be an Array that contains UIe class
        # the type variable lets the code know what turret this is for
        self.UI = [
            UIe(1, (5,5), "blue"),
            UIe(2, (5,65), "yellow"),
            UIe(3, (5,125), "green", renderer=triangle_render),
            UIe(4, (5,185), "brown", renderer=hexagon_render),
        ]

        # init turrets
        self.turrets = []
        self.selectedTurret = Turret(1, -10, -10, self)

        self.gridsize=60

        # Enemies
        self.enemies = []
        self.enemies.append(Enemy(1, (100,100)))

    def draw(self):
        # This func handles anything related to drawing something to the screen
        
        self.screen.fill("darkgray")

        # draw enemies
        for enemy in self.enemies:
            enemy.draw(self)


        # draw current turrets
        for turret in self.turrets:
            turret.draw(self)

        # draw current in hand
        if self.actionRN == "grabturret":

            # change color depending if the turret can be placed
            rectColor = self.selectedTurret.color
            for turret in self.turrets:
                if turret.plzone.colliderect(self.selectedTurret.rect):
                    rectColor = "red"
                    break

            self.selectedTurret.draw(self, rectColor)

        # draw UI
        for UIe in self.UI:
            UIe.draw(self)

        # draw grid lines if SHIFT pressed
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            # draw horizonatally
            for i in range(self.WIDTH//self.gridsize+1):
                pg.draw.line(self.screen, "white", (i*self.gridsize, 0), (i*self.gridsize, self.HEIGHT))

            # draw vertically
            for i in range(self.HEIGHT//self.gridsize+1):
                pg.draw.line(self.screen, "white", (0, i*self.gridsize), (self.WIDTH, i*self.gridsize))

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

            # Set FPS as the name of the window
            pg.display.set_caption(
                str(math.floor(self.clock.get_fps()))+"FPS - TD")

            # if turret in hand update self.selectedTurret
            if self.actionRN == "grabturret":
                t = self.selectedTurret.type
                mx,my = pg.mouse.get_pos()
                
                # if grid lines enabled
                keys = pg.key.get_pressed()
                if keys[pg.K_LSHIFT]:
                    # snap to grid
                    mx=mx+50/2
                    my=my+50/2
                    mx=round(mx/70)*self.gridsize
                    my=round(my/70)*self.gridsize
                    mx=mx-50-(self.gridsize-50)//2
                    my=my-50-(self.gridsize-50)//2
                self.selectedTurret = Turret(t, mx, my, self)

            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = SoftwareRenderer()
    game.run()