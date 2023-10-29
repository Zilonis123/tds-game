import pygame as pg
from ..Visuals.renderers import text
from ..usefulmath import diagonally_pathfind, translate_rect_to_circ
from .bullets import Bullet

class Turret():
    def __init__(self, type, x, y, render):
        self.type = type
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.size = (50,50) # may be subject to change
        self.health = self.maxhealth = 100

        self.cooldown = -1 # if >0 then can shoot
        self.attacking = "none"

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

    def tick(self, render):
        self.cooldown -= 1
        # figure out if we can shoot smth

        if self.attacking == "none":
            # find smth to kill
            self._find_enemy(render)
            # if still nothing .. then damnn
            if self.attacking == "none":
                return
        
        # shoot :)
        if self.cooldown < 0:
            # find dir
            enemy = findenemy_by_id(render, self.attacking)
            if not enemy:
                self.attacking = "none"
                return
            direction = diagonally_pathfind(self.rect.center, enemy.rect.center)

            # create bullet
            b = Bullet(direction[0], direction[1], self.rect.center, 1)
            render.bullets.append(b)

            # cooldown
            self.cooldown = 1000000
    
    def draw(self, render, color="none"):
        if color == "none":
            color = self.color
        self.renderer(render, self.rect, color)
        # if selected draw outline
        if render.selectedTurret == self:
            self.renderer(render, self.rect, "white", 3)
        if self.health < self.maxhealth:
            text(render, str(self.health), "white", self.rect.center, size=15)

    def damage(self, render, damage):
        self.health -= damage

        # ideally here we would show that this tower is getting damaged

        if self.health <= 0:
            # ded
            render.turrets.remove(self)
    
    def _find_enemy(self, render, ignore=[]):
        target = "none"
        targetdiff = (999, 999)
        for enemy in render.enemies:
            if enemy.uid in ignore:
                continue

            difference = (abs(enemy.rect.center[0]-self.rect.center[0]), 
            abs(enemy.rect.center[1]-self.rect.center[1]))

            if difference < targetdiff:
                targetdiff = difference
                target = enemy.uid
        if target != "none":
            self.attacking = target

    def __eq__(self, other):
        if isinstance(other, Turret):
            return self.uid == other.uid
        return False

def addTurret(render, t):
    render.turrets.append(t)


def findenemy_by_id(render, uid):
    enemy = [enemy for enemy in render.enemies if enemy.uid == uid]
    if len(enemy) == 0:
        return False

    # we can assume that theres only ever going to be 1 turret by that UId since no 2 turrets
    # can be in the same x,y coordinates at once
    # also to insure that isnt the case the uids are taking to factor the type of the
    # turret
    return enemy[0]
