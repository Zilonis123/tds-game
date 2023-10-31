from ..Visuals.renderers import circle_renderer, healthbar, text
import pygame as pg
from ..usefulmath import diagonally_pathfind

from .Enemies.enemycollisions import *
from .Enemies.enemytargets import *

import math
import random

class Enemy():
    def __init__(self, type, pos, renderer=circle_renderer):
        self.type = type
        self.pos = pos
        self.health = 100
        self.maxhealth = 100
        self.renderer = renderer

        self.speed = 2

        self.cooldown = -1 # if higher than 0 cant attack
        self.strength = 10

        self.rect = pg.Rect(pos, (30,30))

        # UId
        tuple_str = ''.join(map(str, self.pos))
        self.uid = tuple_str + str(self.type) + str(int(random.uniform(0.0, 1000.0)))


        self.targetTurret = None

        if type==1:
            self.color = "darkgreen"

    def draw(self, render):
        self.renderer(render, self.rect, self.color)
        self.renderer(render, self.rect, "black", 1)

        # healthbar
        # only display healthbar if its smaller than max health
        if self.health < self.maxhealth:
            healthbar(render, (self.rect.center[0], self.rect.center[1]-20), self.health, self.maxhealth)

    def tick(self, render):
        # tick cooldown
        self.cooldown -= 1
        self._move_to_turret(render)

    
 
    def _move_to_turret(self, render):
        if self.targetTurret == None:
            # search for a turret that's the closest to the enemy
            turret = find_turret(self, render)
            if turret != None:
                self.targetTurret = turret.uid

        if self.targetTurret == None:
            return

        # if we have a turret selected go attack it

        # for precausion let's check if the turret exists
        turret = findturret_by_id(render, self.targetTurret)
        if not turret:
            # no turret by that id was found
            # meaning the turret was deleted or destroyed
            self.targetTurret = None
            return
        
        # check if we can move
        # if we have collided return
        if turret.rect.colliderect(self.rect):
            # this is where we would deal damage to the turret
            if self.cooldown < 0:
                turret.damage(render, self.strength)

                # 60 = 1s
                # 30 = .5s
                self.cooldown = 30
            return

        direction = diagonally_pathfind(self.rect.center, turret.rect.center)
        direction = (round(direction[0]*self.speed), round(direction[1]*self.speed))
        self.rect = self.rect.move(direction[0], direction[1])

        # check for collisions
        
        check_collisions(self, render)

    def damage(self, render, damage):
        self.health -= damage
        if self.health < 0:
            # ded
            render.enemies.remove(self)
            return

    def __eq__(self, other):
        if isinstance(other, Enemy):
            return self.uid == other.uid
        return 

    


def h_v_pathfind(position1, position2):
    # horizontal and vertically .. dont allow diagonalls
    delta_x = position2[0] - position1[0]
    delta_y = position2[1] - position1[1]

    # Calculate the direction while only allowing horizontal and vertical movement
    if abs(delta_x) != 0:
        if abs(delta_x) < 1:
            direction = (delta_x, 0)
        else:
            direction = (1 if delta_x > 0 else -1, 0)
    else:
        # Move vertically
        direction = (0, 1 if delta_y > 0 else -1)


    return direction

def findturret_by_id(render, uid):
    turret = [turret for turret in render.turrets if turret.uid == uid]
    if len(turret) == 0:
        return False

    # we can assume that theres only ever going to be 1 turret by that UId since no 2 turrets
    # can be in the same x,y coordinates at once
    # also to insure that isnt the case the uids are taking to factor the type of the
    # turret
    return turret[0]