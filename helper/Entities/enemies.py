from ..Visuals.renderers import circle_renderer, healthbar, text
import pygame as pg
from .turrets import findturret_by_id
import math

class Enemy():
    def __init__(self, type, pos, renderer=circle_renderer):
        self.type = type
        self.pos = pos
        self.health = 100
        self.maxhealth = 100
        self.renderer = renderer

        self.speed = 2

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
        
        # check if we can move
        # if we have collided return
        if turret.rect.colliderect(self.rect):
            # this is where we would deal damage to the turret
            return

        # for debug lets draw a line from the enemy to the turret
        pg.draw.line(render.screen, "red", self.rect.center, turret.rect.center, 4)

        direction = h_v_pathfind(self.rect.center, turret.rect.center)
        
        self.rect = self.rect.move(direction[0], direction[1])

        # check for collisions
        # NOTE: currently only checks the target turret

        if turret.rect.colliderect(self.rect):
            print("collided with " + str(turret.uid))
            return

        # debug text direction
        text(render, str(direction), "white", self.rect.center)

    def __eq__(self, other):
        if isInstance(other, Enemy):
            return self.uid == other.uid
        return 

def diagonally_pathfind(b, a):
    dx = a[0] - b[0]
    dy = a[1] - b[1]

    dx = round(dx)
    dy = round(dy)

    magnitude = math.sqrt(dx**2 + dy**2)

    if 2 > magnitude < 2:
        # If the positions are the same, return (0, 0)
        direction = (0, 0)
    else:
        direction = (round(dx / magnitude), round(dy / magnitude))
    
    return direction


def h_v_pathfind(position1, position2):
    # horizontal and vertically .. dont allow diagonalls
    delta_x = position2[0] - position1[0]
    delta_y = position2[1] - position1[1]

    # Calculate the direction while only allowing horizontal and vertical movement
    if abs(delta_x) != 0:
        # Move horizontally
        direction = (1 if delta_x > 0 else -1, 0)
    else:
        # Move vertically
        direction = (0, 1 if delta_y > 0 else -1)


    return direction