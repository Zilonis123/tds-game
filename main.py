import pygame as pg
import math
from controlls import *
from turrets import Turret

class SoftwareRenderer():

    def __init__(self):
        pg.init()
        self.RES = self.WIDHT, self.HEIGHT = 160*5, 90*5
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.FPS = 60
        
        self.actionRN = "none"

        self.turrets = []
        self.handturret = Turret(1, -10, -10)

    def draw(self):
        # Handles anything related to drawing something to the screen
        self.screen.fill("purple")

        # UI
        r = pg.Rect(10,10,50,50)
        pg.draw.rect(self.screen, "blue", r)
        r = pg.Rect(10,70,50,50)
        pg.draw.rect(self.screen, "yellow", r)


        # draw current turrets
        for turret in self.turrets:
            turret.draw(self)

        # draw current in hand
        if self.actionRN == "grabturret":

            # change color depending if the turret can be placed
            rectColor = "green"
            for turret in self.turrets:
                if turret.plzone.colliderect(self.handturret.rect):
                    rectColor = "red"
                    break

            self.handturret.draw(self, rectColor)


        


    def handleEvents(self):
        # Handles pygame events

        for event in pg.event.get():
            if event.type == pg.QUIT: 
                self.running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_click(self)

    def run(self):

        self.running = True
        while self.running:

            self.draw()
            self.handleEvents()

            # Set FPS as the name of the window
            pg.display.set_caption(
                str(math.floor(self.clock.get_fps()))+"FPS - TD")

            # if turret in hand update self.handturret
            if self.actionRN == "grabturret":
                t = self.handturret.type
                mx,my = pg.mouse.get_pos()
                self.handturret = Turret(t, mx, my)

            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = SoftwareRenderer()
    game.run()