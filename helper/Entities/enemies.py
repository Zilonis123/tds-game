from ..Visuals.renderers import circle_renderer, healthbar, text
import pygame as pg
from .turrets import Turret

class Enemy():
    def __init__(self, type, pos, renderer=circle_renderer):
        self.type = type
        self.pos = pos
        self.health = 100
        self.maxhealth = 100
        self.renderer = renderer

        self.rect = pg.Rect(pos, (30,30))

        # UId
        tuple_str = ''.join(map(str, self.pos))
        self.uid = tuple_str + str(self.type)

        self.targetTurret = "none"

        if type==1:
            self.color = "darkgreen"

    def draw(self, render):
        self.renderer(render, self.rect, self.color)
        self.renderer(render, self.rect, "black", 1)

        # healthbar
        healthbar(render, (self.rect.center[0], self.rect.center[1]-20), self.health, self.maxhealth)

    def tick(self, render):
        if self.targetTurret == "none":
            # search for a turret
            target = Turret(1, -999, -999, render)
            targetdiff = (999, 999)
            for turret in render.turrets:
                difference = (abs(turret.pos[0]-self.pos[0]), abs(turret.pos[1]-self.pos[1]))

                if difference < targetdiff:
                    targetdiff = difference
                    target = turret
            pg.draw.rect(render.screen, "black", pg.Rect(target.pos, (50, 50)))
            text(render, str(targetdiff), "white", target.pos, size=15)



    def __eq__(self, other):
        if isInstance(other, Enemy):
            return self.uid == other.uid
        return 