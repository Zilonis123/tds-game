from ..Visuals.renderers import circle_renderer, healthbar, text
import pygame as pg
from ..usefulmath import diagonally_pathfind, findturret_by_id

from .Enemies.enemycollisions import *
from .Enemies.enemytargets import *

from .turrets import Turret

from .Enemies.enemypathfind import astar_pathfinding, draw_path

import sys
from loguru import logger

import math
from random import uniform

class Enemy():
    def __init__(self, type: int, pos: tuple[int | float, int | float], renderer=circle_renderer):
        self.type = type
        self.pos: tuple[int | float, int | float] = pos
        self.health: int = 100
        self.maxhealth: int = 100
        self.renderer = renderer

        self.speed: int | float = 2

        self.path: list = []
        self.pathstart: tuple[int|float, int|float] | None = None

        self.cooldown: int = -1 # if higher than 0 cant attack
        self.strength: int = 10

        self.rect: pg.Rect = pg.Rect(pos, (30,30))

        # UId
        tuple_str: str = ''.join(map(str, self.pos))
        self.uid: str = tuple_str + str(self.type) + str(int(uniform(0.0, 1000.0)))


        self.targetTurret: str | None  = None

        if type==1:
            self.color: str = "darkgreen"

    def draw(self, render):
        self.renderer(render, self.rect, self.color)
        # self.renderer(render, self.rect, "black", 1)

        # healthbar
        # only display healthbar if its smaller than max health
        if self.health < self.maxhealth:
            healthbar(render, (self.rect.center[0], self.rect.center[1]-20), self.health, self.maxhealth)

        # if we are selected draw more shit
        if render.selectedEnemy == self:
            text(render, f"Target {self.targetTurret}", "black", self.rect.topright, type="topleft", font="Gobold.otf")

            if self.path != []:
                draw_path(render.screen, self.path, self.pathstart, 5)

            self.renderer(render, self.rect, "white", 2)



    def tick(self, render):
        # tick cooldown
        self.cooldown -= 1
        self._move_to_turret(render)

    def change_target(self, target: str):
        self.path = []
        self.targetTurret = target
    
 
    def _move_to_turret(self, render):
        if self.targetTurret == None:
            # search for a turret that's the closest to the enemy
            turret: str = find_turret(self, render)
            if turret != None:
                self.targetTurret = turret.uid

        if self.targetTurret == None:
            return

        # if we have a turret selected go attack it

        # for precausion let's check if the turret exists
        turret = findturret_by_id(render, self.targetTurret)
        if turret == None:
            # no turret by that id was found
            # meaning the turret was deleted or destroyed
            self.targetTurret = None

            self.path = []
            return
        
        # check if we can move
        # if we have collided return
        if turret.rect.colliderect(self.rect):
            if self.cooldown < 0:
                turret.damage(render, self.strength)

                self.path = []
                self.cooldown = 30
            return

        if self.path == []:
            self.path = astar_pathfinding(self.rect.center, turret.rect.center, 1)
            if self.path != []:
                self.pathstart = self.rect.center
            else:
                return

        direction: tuple[int,int] = self.path.pop()

        self.rect: pg.Rect = self.rect.move(direction[0], direction[1])

        # check for collisions
        
        #check_collisions(self, render)

    def damage(self, render, damage):
        self.health -= damage
        if self.health < 0:
            # ded
            render.enemies.remove(self)
            if render.selectedEnemy == self:
                render.selectedEnemy = None
            return

    def __eq__(self, other):
        if isinstance(other, Enemy):
            return self.uid == other.uid
        return 

    

