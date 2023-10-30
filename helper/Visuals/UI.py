import pygame as pg
from ..usefulmath import translate_rect_to_circ
from .renderers import square_render
from ..Entities.turrets import Turret

# UIe - UI element
class UIe:
    def __init__(self, type, pos, color, turret="none", renderer=square_render):
        self.pos = pos
        self.color = pg.Color(color) # Use pygame Color because its better
        self.top = pos[0]
        self.left = pos[1]

        self.isTurretspawn = isinstance(type, int)
        self.type = type
        self.rect = pg.Rect(pos, (50,50))
        self.renderer = renderer

        self.presscost = 100 # how much money do we steal from u if yu press the button

        # delete logic
        self.turret = turret
        if self.type == "delete":

            # "Hitbox"
            self.rect = pg.Rect(pos, (30,30))
            self.rect = pg.Rect(translate_rect_to_circ(self.rect), (self.rect.w, self.rect.h))

    def draw(self, render):
        if self.type == "delete":
            pg.draw.circle(render.screen, self.color, self.pos, 15) # draw circle
            pg.draw.circle(render.screen, "black", self.pos, 15, 2) # draw outline
            # draw a X
            # self.pos - circle center
            pg.draw.line(render.screen, "white", (self.top+8, self.left+8), (self.top-8, self.left-8), 3)
            pg.draw.line(render.screen, "white", (self.top-8, self.left+8), (self.top+8, self.left-8), 3)
        else:
            self.renderer(render, self.rect, self.color)

    def action(self, render):
        if self.isTurretspawn:
            # grab turret
            mx,my = pg.mouse.get_pos()

            render.actionRN = "grabturret"
            render.selectedTurret = Turret(self.type, mx, my, render)

            render.cash -= self.presscost
        elif self.type == "delete":
            render.turrets.remove(self.turret)
            render.UI.remove(self)
            render.actionRN = "none"
            render.selectedTurret = "none"
        