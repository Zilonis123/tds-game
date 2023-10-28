import pygame as pg
from .usefulmath import translate_rect_to_circ

class UIe:
    def __init__(self, type, pos, color, turret="none"):
        self.pos = pos
        self.color = color
        self.top = pos[0]
        self.left = pos[1]

        self.isTurretspawn = isinstance(type, int)
        self.type = type
        self.rect = pg.Rect(pos, (50,50))
        self.render = "rect"


        # delete logic
        self.turret = turret
        if self.type == "delete":
            self.render = "circle"
            self.rect = pg.Rect(translate_rect_to_circ(self.rect), (30,30))

    def draw(self, render):
        if self.render == "circle":
            pg.draw.circle(render.screen, self.color, self.pos, 15) # draw circle
            pg.draw.circle(render.screen, "black", self.pos, 15, 2) # draw outline
            if self.type == "delete":
                # draw a X
                # self.pos - circle center
                pg.draw.line(render.screen, "white", (self.top+8, self.left+8), (self.top-8, self.left-8), 3)
                pg.draw.line(render.screen, "white", (self.top-8, self.left+8), (self.top+8, self.left-8), 3)
        else:
            pg.draw.rect(render.screen, self.color, self.rect)

    def action(self, render):
        if self.type == "delete":
            render.turrets.remove(self.turret)
            render.UI.remove(self)
            render.actionRN = "none"