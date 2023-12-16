from ..Visuals.renderers import circle_renderer, healthbar, text, draw_circle_alpha
import pygame as pg
from ..usefulmath import findturret_by_id, multiplyTuple, changeTuple
from .Enemies.enemycollisions import *
from .Enemies.enemytargets import *
from .turrets import Turret
from .Enemies.enemypathfind import astar_pathfinding, draw_path

import sys, math, json
from loguru import logger
from random import uniform

class Enemy():
    def __init__(self, type: str, pos: tuple[int, int], renderer=circle_renderer):
        self.type: str = type
        self.pos: tuple[int, int] = pos
        self.renderer = renderer


        self.path: list = []
        self.pathstart: tuple[int|float, int|float] | None = None

        
        self.x = pos[0]
        self.y = pos[1]
        self.size = 30
        self.rect: pg.Rect = pg.Rect(pos, (self.size,self.size))

        # UId
        tuple_str: str = ''.join(map(str, self.pos))
        self.uid: str = tuple_str + str(self.type) + str(int(uniform(0.0, 1000.0)))


        self.targetTurret: str | None  = None

        # default values
        self.health= self.maxhealth = 100
        self.speed: int = 2
        self.cooldown: int = -1
        self.strength: int = 10
        self.cooldown_increase = 30
        self.color = "black"

        # get info about ourselfes
        f = open("info/enemies.json")
        data = json.load(f)
        data = data.get(type, None)

        if data != None:
            self.health = self.maxhealth = data["health"]
            self.strength: int = data["damage"]
            self.speed: float = data["speed"]
            self.cooldown_increase: int = data["cooldown"]
            self.color = data["color"]
    
        

    def draw(self, render):
        # draw shadow
        draw_circle_alpha(render, pg.Color(0,0,0,65), changeTuple(self.rect.center, (self.size//8, self.size//7)), 15)
        self.renderer(render, self.rect, self.color)
        self.renderer(render, self.rect, "black", width=2)

        
        # if we are selected draw more shit
        if render.selectedEnemy == self:
            text(render, f"Target {self.targetTurret}", "black", self.rect.topright, type="topleft", font="Gobold.otf")

            if self.path != []:
                draw_path(render.screen, self.path, self.pathstart, 5)

            self.renderer(render, self.rect, "white", 2)

    def draw_after(self, render):
        # healthbar
        # only display healthbar if its smaller than max health
        if self.health < self.maxhealth:
            healthbar(render, (self.rect.center[0], self.rect.center[1]-20), self.health, self.maxhealth)



    def tick(self, render):
        # tick cooldown
        self.cooldown -= 1
        self._move_to_turret(render)
        if self.type == "strong":
            pass

    def change_target(self, target: str):
        self.path = []
        self.targetTurret = target

        
    
 
    def _move_to_turret(self, render):
        if self.targetTurret == None:
            # search for a turret that's the closest to the enemy
            turret: str = find_turret(self, render)
            if turret == None:
                return
            self.targetTurret = turret.uid

        # if we have a turret selected go attack it

        # for precausion let's check if the turret exists
        turret = findturret_by_id(render, self.targetTurret)
        if turret == None:
            self.targetTurret = None
            self.path = []
            return
        
        # check if we can move
        # if we have collided return
        if turret.rect.colliderect(self.rect):
            if self.cooldown < 0:
                turret.damage(render, self.strength)

                self.path = []
                self.cooldown = self.cooldown_increase
            return

        if self.path == []:
            self.path = astar_pathfinding(self.rect.center, turret.rect.center, self.speed)
            if self.path != []:
                self.pathstart = self.rect.center
            else:
                return

        direction: tuple[float,float] = self.path.pop()
        self.x, self.y = changeTuple((self.x, self.y), direction)
        
        self.rect.x = self.x
        self.rect.y = self.y

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

    

