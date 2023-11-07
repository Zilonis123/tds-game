import pygame as pg
from ..Visuals.renderers import text, draw_circle_alpha
from ..usefulmath import diagonally_pathfind, adjust_color, pointInCircle, findenemy_by_id
from .bullets import Bullet
import math

class Turret():
    def __init__(self, type, x, y, render):
        self.type = type
        self.pos: tuple[int|float,int|float] = (x,y)
        self.size: tuple[int, int] = (50,50) # may be subject to change
        self.health: int = 100
        self.maxhealth: int = 100

        self.cooldown: int = -1 # if >0 then can shoot
        self.attacking: None|str = None # stores uid

        # stats
        self.kills: int = 0
        self.damagedealt: int = 0

        self.turretheadclr: int = 50 # this is not the color, but the difference in the color between the body
        # positive = lighter 
        # negative = darker

        # figure out the turrets cooldown increase

        # range - radius of the "range" circle


        self.cIncrease: int
        self.strenght: int
        self.bSpeed: int
        self.range: int
        self.health: int
        self.maxhealth: int


        if type == 1:
            self.cIncrease = 15
            self.strenght = 7
            self.bSpeed = 10
            self.range = 120
            self.health = self.maxhealth = 200
        elif type == 2:
            self.cIncrease = 60
            self.range = 0
            self.health = self.maxhealth = 75
            self.turretheadclr = 0
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
        


        self.headangle: int = 0

        self.rect: pg.Rect = pg.Rect(self.pos, self.size)
        dz = 10 # deadzone -- extra pixels where nothing can be palced
        self.plzone: pg.Rect = pg.Rect((x-dz,y-dz), (self.size[0]+dz*2, self.size[1]+dz*2)) # zone where no turret can be placed

        # generatate an UId
        tuple_str: str = ''.join(map(str, self.pos))
        self.uid: str = tuple_str + str(self.type)

        # choose color
        for UIe in render.UI:
            if UIe.type == type:
                self.color: tuple[int,int,int,int] = UIe.color
                self.renderer = UIe.renderer
                break

    def tick(self, render):
        self.cooldown -= 1
        # figure out if we can shoot smth

        if self.type != 2: tick_turret(self, render)
        else: tick_farm(self, render)
    
    def draw(self, render, color=None):
        if color == None:
            color = self.color
        self.renderer(render, self.rect, color)


        # draw turret head
        self._draw_head(render, color)


        # draw health
        if self.health < self.maxhealth:
            text(render, str(self.health), "white", self.rect.center, size=15)

        # if selected draw outline and range
        if render.selectedTurret == self:
            self.renderer(render, self.rect, "white", 3)
            color: pg.Color = pg.Color(255, 255, 255, 100)
            draw_circle_alpha(render, color, self.rect.center, radius=self.range)

            # display stats
            if render.actionRN != "grabturret":
                text(render, f"Kills: {self.kills}", "black", (self.rect.topleft[0]-100, self.rect.topleft[1]), 
                type="topleft", font="fonts/Gobold.otf")

                text(render, f"Damage: {self.damagedealt}", "black", (self.rect.topleft[0]-100, self.rect.topleft[1]+20),
                type="topleft", font="fonts/Gobold.otf")

                text(render, f"UId: {self.uid}", "black", (self.rect.topright[0]+10, self.rect.topright[1]+20),
                type="topleft", font="fonts/Gobold.otf")

    def _draw_head(self, render, color):
        size: tuple[int|float, int|float] = (self.rect.w//2, self.rect.h//2)
        pos: tuple[int|float, int|float] = (self.rect.center[0]-size[0]//2, self.rect.center[1]-size[1]//2)

        if self.type == 3:
            # triangle offset
            pos = (pos[0], pos[1]+10)
        
        headrect: pg.Rect = pg.Rect(pos, size)
        if self.attacking != None:
            # calculate the angle
            e = findenemy_by_id(render, self.attacking) # Enemy class
            if not e:
                self.attacking != None
            else:
                x1,y1 = e.rect.center
                x2,y2 = headrect.center
                dy: float = x2 - x1
                dx: float = y2 - y1

                # Calculate the angle in radians
                angle_radians = math.atan2(dy, dx)

                # Convert the angle to degrees if needed
                angle_degrees = math.degrees(angle_radians)

                # Ensure the angle is between 0 and 360 degrees
                self.headangle = (angle_degrees + 360) % 360

        color: pg.Color = adjust_color(color, self.turretheadclr)

        self.renderer(render, headrect, color, rotation_angle=self.headangle)

    def damage(self, render, damage):
        self.health -= damage

        # ideally here we would show that this tower is getting damaged

        if self.health <= 0:
            # ded
            render.turrets.remove(self)
            if render.selectedTurret == self:
                render.selectedTurret = None
                for UI in render.UI:
                    if UI.turret == self:
                        render.UI.remove(UI)

                
    
    def _find_enemy(self, render, ignore=[]):
        target: None | str = None
        targetdiff: tuple[int|float, int|float] = (999, 999)
        for enemy in render.enemies:
            if enemy.uid in ignore:
                continue

            in_range: bool = pointInCircle(enemy.rect.center, self.rect.center, self.range)

            if not in_range:
                continue

            difference: tuple[int|float, int|float] = (abs(enemy.rect.center[0]-self.rect.center[0]), 
            abs(enemy.rect.center[1]-self.rect.center[1]))

            if difference < targetdiff:
                targetdiff = difference
                target: str = enemy.uid
        if target != None:
            self.attacking: str = target

    def __eq__(self, other):
        if isinstance(other, Turret):
            return self.uid == other.uid
        return False

def addTurret(render, t: Turret):
    render.turrets.append(t)



def tick_turret(self, render):
    if self.attacking == None:
        # find smth to kill
        self._find_enemy(render)
        # if still nothing .. then damnn
        if self.attacking == None:
            return

    # shoot 
    if self.cooldown < 0:
        # find dir
        enemy = findenemy_by_id(render, self.attacking)
        if not enemy:
            self.attacking = None
            return

        can_shoot = pointInCircle(enemy.rect.center, self.rect.center, self.range)

        if not can_shoot:
            return

        direction = diagonally_pathfind(self.rect.center, enemy.rect.center)

        # create bullet
        b = Bullet(direction[0], direction[1], self.rect.center, self.cIncrease, self.bSpeed, turret=self)
        render.bullets.append(b)

        # cooldown
        self.cooldown = self.cIncrease


def tick_farm(self, render):

    if self.cooldown < 0:
        render.addcash(50)

        self.cooldown = 240