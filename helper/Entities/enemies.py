from ..Visuals.renderers import circle_renderer, healthbar, text
import pygame as pg
from .turrets import Turret, findturret_by_id

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
            # search for a turret that's the closest to the enemy
            # isnt 100% effective
            # may need improvement
            target = "none"
            targetdiff = (999, 999)
            for turret in render.turrets:
                difference = (abs(turret.pos[0]-self.pos[0]), abs(turret.pos[1]-self.pos[1]))

                if difference < targetdiff:
                    targetdiff = difference
                    target = turret.uid
            if target != "none":
                self.targetTurret = target
            else:
                return

        # if we have a turret selected go attack it

        # for precausion let's check if the turret exists
        turret = findturret_by_id(render, self.targetTurret)
        if not turret:
            # no turret by that id was found
            # meaning the turret was deleted or destroyed
            self.targetTurret = "none"
            return
        
        # for debug lets draw a line from the enemy to the turret
        pg.draw.line(render.screen, "red", self.rect.center, turret.rect.center, 4)



    def __eq__(self, other):
        if isInstance(other, Enemy):
            return self.uid == other.uid
        return 