import pygame as pg
from ..Visuals.renderers import circle_renderer

class Bullet():
    def __init__(self, spx, spy, pos, strength):
        self.spx = spx
        self.spy = spy
        self.strength = strength
        self.rect = pg.Rect(pos, (18,18))

    def tick(self, render):
        # move
        self.rect = self.rect.move(self.spx, self.spy)

        outofbounds = self.rect.x > render.WIDTH or self.rect.x < 0 or self.rect.y > render.HEIGHT or self.rect.y < 0
        if outofbounds:
            render.bullets.remove(self)
            return
        
        # collisions
        for enemy in render.enemies:
            enemy.damage(render, self.strength)

            # we are ded
            render.bullets.remove(self)
            return
        

    def draw(self, render):
        circle_renderer(render, self.rect, "yellow", radius=self.rect.width//2)