import pygame as pg
from ..Visuals.renderers import text, draw_circle_alpha
from ..usefulmath import diagonally_pathfind, adjust_color
from .bullets import Bullet
import math

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

        self.turretheadclr = 50 # this is not the color, but the difference in the color between the body
        # positive = lighter 
        # negative = darker

        # figure out the turrets cooldown increase
        if type == 1:
            self.cIncrease = 15
            self.strenght = 7
            self.bSpeed = 10
            self.range = 120
            self.health = self.maxhealth = 200
        elif type == 3:
            self.cIncrease = 60
            self.strenght = 15
            self.bSpeed = 30
            self.range = 230
            self.health = self.maxhealth = 50
            self.turretheadclr = -100
        elif type == 4:
            self.cIncrease = 30
            self.strenght = 10
            self.bSpeed = 12
            self.range = 150
            self.health = self.maxhealth = 100


        self.headangle = 0

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

            d = math.sqrt((enemy.rect.center[0] - self.rect.center[0])**2+(enemy.rect.center[1] - self.rect.center[1]) ** 2)
            can_shoot = d <= self.range

            if not can_shoot:
                return

            direction = diagonally_pathfind(self.rect.center, enemy.rect.center)

            # create bullet
            b = Bullet(direction[0], direction[1], self.rect.center, self.cIncrease, self.bSpeed)
            render.bullets.append(b)

            # cooldown
            self.cooldown = self.cIncrease
    
    def draw(self, render, color="none"):
        if color == "none":
            color = self.color
        self.renderer(render, self.rect, color)


        # draw turret head
        size = (self.rect.w//2, self.rect.h//2)
        pos = (self.rect.center[0]-size[0]//2, self.rect.center[1]-size[1]//2)

        if self.attacking != "none":
            # calculate the angle
            e = findenemy_by_id(render, self.attacking)
            if not e:
                return
            x1,y1 = e.rect.center
            x2,y2 = self.rect.center
            dy = x2 - x1
            dx = y2 - y1

            # Calculate the angle in radians
            angle_radians = math.atan2(dy, dx)

            # Convert the angle to degrees if needed
            angle_degrees = math.degrees(angle_radians)

            # Ensure the angle is between 0 and 360 degrees
            self.headangle = (angle_degrees + 360) % 360

        color = adjust_color(self.color, self.turretheadclr)
        headrect = pg.Rect(pos, size)
        self.renderer(render, headrect, color, rotation_angle=self.headangle)


        # draw health
        if self.health < self.maxhealth:
            text(render, str(self.health), "white", self.rect.center, size=15)

        # if selected draw outline
        if render.selectedTurret == self:
            self.renderer(render, self.rect, "white", 3)
            color = pg.Color(255, 255, 255, 100)
            draw_circle_alpha(render, color, self.rect.center, radius=self.range)

    def damage(self, render, damage):
        self.health -= damage

        # ideally here we would show that this tower is getting damaged

        if self.health <= 0:
            # ded
            render.turrets.remove(self)
            if render.selectedTurret == self:
                render.selectedTurret = "none"
                for UI in render.UI:
                    if UI.turret == self:
                        render.UI.remove(UI)

                
    
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
