import pygame as pg
from ..Visuals.renderers import text

class Turret():
    def __init__(self, type, x, y, render):
        self.type = type
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.size = (50,50) # may be subject to change
        self.health = self.maxhealth = 100

        self.rect = pg.Rect(self.pos, self.size)
        dz = 10 # deadzone -- extra pixels where nothing can be palced
        self.plzone = pg.Rect((x-dz,y-dz), (self.size[0]+dz*2, self.size[1]+dz*2)) # zone where no turret can be placed

        # generatate an UId
        tuple_str = ''.join(map(str, self.pos))
        self.uid = tuple_str + str(self.type)

        # choose color
        for UIe in render.UI:
            if UIe.type == type:
                self.color = UIe.color
                self.renderer = UIe.renderer
    
    def draw(self, render, color="none"):
        if color == "none":
            color = self.color
        self.renderer(render, self.rect, color)
        # if selected draw outline
        if render.selectedTurret == self:
            self.renderer(render, self.rect, "white", 3)
        if self.health < self.maxhealth:
            text(render, str(self.health), "white", self.rect.center, size=15)

    def __eq__(self, other):
        if isinstance(other, Turret):
            return self.uid == other.uid
        return False

def addTurret(render, t):
    render.turrets.append(t)


def findturret_by_id(render, uid):
    turret = [turret for turret in render.turrets if turret.uid == uid]
    if len(turret) == 0:
        return False

    # we can assume that theres only ever going to be 1 turret by that UId since no 2 turrets
    # can be in the same x,y coordinates at once
    # also to insure that isnt the case the uids are taking to factor the type of the
    # turret
    return turret[0]