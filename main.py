import pygame as pg
import math

from helper.controlls import *
from helper.UI import UIe
from helper.turrets import Turret

class SoftwareRenderer():

    def __init__(self):
        pg.init()
        self.RES = self.WIDHT, self.HEIGHT = 160*5, 90*5
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.FPS = 60
        
        self.actionRN = "none"


        # UI
        # This will be an Array that contains UIe class
        # the type variable lets the code know what turret this is for
        self.UI = [
            UIe(1, (10,10), "blue"),
            UIe(2, (10,75), "yellow"),
            UIe(3, (10,140), "green"),
        ]

        # init turrets
        self.turrets = []
        self.selectedTurret = Turret(1, -10, -10, self)

    def draw(self):
        # This func handles anything related to drawing something to the screen
        
        self.screen.fill("purple")


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

            # Set FPS as the name of the window
            pg.display.set_caption(
                str(math.floor(self.clock.get_fps()))+"FPS - TD")

            # if turret in hand update self.selectedTurret
            if self.actionRN == "grabturret":
                t = self.selectedTurret.type
                mx,my = pg.mouse.get_pos()
                self.selectedTurret = Turret(t, mx, my, self)

            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = SoftwareRenderer()
    game.run()