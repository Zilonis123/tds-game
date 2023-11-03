import pygame as pg
from ..usefulmath import translate_rect_to_circ
from .renderers import square_render, text
from ..Entities.turrets import Turret

# UIe - UI element
class UIe:
    def __init__(self, type, pos, color, turret=None, renderer=square_render):
        self.pos = pos
        self.color = pg.Color(color) # Use pygame Color because its better
        self.top = pos[0]
        self.left = pos[1]

        self.isTurretspawn = isinstance(type, int)
        self.type = type
        self.rect = pg.Rect(pos, (50,50))
        self.renderer = renderer

        self.cost = 100

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
            color = "GREEN"
            if render.cash < self.cost:
                color = "RED"
            
            text(render, str(self.cost), color, (self.rect.centerx, self.rect.centery+(self.rect.h//3*2)),
             font="fonts/Gobold.otf")
            

    def action(self, render):
        if self.isTurretspawn:
            if render.cash < self.cost:
                return
            # grab turret
            mx,my = pg.mouse.get_pos()

            render.actionRN = "grabturret"
            render.selectedTurret = Turret(self.type, mx, my, render)

            render.cash -= self.cost
            render.ttext.append({"cash": -self.cost, "time": 0})
        elif self.type == "delete":
            render.turrets.remove(self.turret)
            render.UI.remove(self)
            render.actionRN = "none"
            render.selectedTurret = "none"
        