from ..Visuals.renderers import circle_renderer, healthbar, text
import pygame as pg
from ..usefulmath import diagonally_pathfind

from .Enemies.enemycollisions import *
from .Enemies.enemytargets import *

from helper.Entities.Enemies.enemypathfind import astar_pathfinding, draw_path

import sys
from loguru import logger

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

        self.path: list | None = None
        self.pathstart = None
        self.pastPath = False
        self.pathon = 0

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

            self.path = None
            return
        
        # check if we can move
        # if we have collided return
        if turret.rect.colliderect(self.rect):
            if self.cooldown < 0:
                turret.damage(render, self.strength)

                self.path = None
                self.cooldown = 30
            return

        # direction = diagonally_pathfind(self.rect.center, turret.rect.center)


        rect_values = []
    
        # # Extract "rect" values from the first list
        # for t in render.turrets:
        #     if t.uid != self.targetTurret:
        #         rect_values.append(t.rect)
        
        # # Extract "rect" values from the second list
        # for e in render.enemies:
        #     if e != self:
        #         rect_values.append(e.rect)

        if self.path != None and self.pathon+1 > len(self.path):
            self.path = None

        if self.path == None:
            #check_collisions(self, render)

            path = None
            dist = 10000
            distToT = math.hypot(self.rect.centerx - turret.rect.centerx, self.rect.centery - turret.rect.centery)
            for p in render.enemypathcache:
                if p["end"] == turret.rect.center:

                    _a = math.hypot(self.rect.centerx - p["start"][0], self.rect.centery - p["start"][1])

                    if distToT+20 > p["distToTurret"]+_a and dist > p["distToTurret"]+_a:
                        
                        temp = astar_pathfinding(rect_values, self.rect.center, p["start"], self.speed)
                        path = temp+p["path"]
                        dist = p["distToTurret"]+_a

            if path == None:
                self.path = astar_pathfinding(rect_values, self.rect.center,turret.rect.center, self.speed)

                self.pastPath = False


                render.enemypathcache.append({
                    "path": self.path,
                    "end": turret.rect.center,
                    "start": self.rect.center,
                    "distToTurret": distToT
                })
            else:
                self.path = path
                self.pastPath = True
            
            self.pathstart = self.rect.center
            self.pathon = 0

            s = sys.getsizeof(render.enemypathcache)
            logger.info(f"enemy cache takes up {s} bytes")

    
            if not self.path:
                return

        draw_path(render.screen, self.path, self.pathstart, 5, self.pastPath)
        direction = self.path[self.pathon]
        self.pathon += 1

        direction = (round(direction[0]), round(direction[1]))



        self.rect = self.rect.move(direction[0], direction[1])

        # check for collisions
        
        #check_collisions(self, render)

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

    



def findturret_by_id(render, uid):
    turret = [turret for turret in render.turrets if turret.uid == uid]
    if len(turret) == 0:
        return False

    return turret[0]