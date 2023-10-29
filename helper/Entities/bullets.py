import pygame as pg
from ..Visuals.renderers import circle_renderer

class Bullet():
    def __init__(self, spx, spy, pos, strength):
        self.spx = spx
        self.spy = spy
        self.speed = 10
        self.x, self.y = pos
        self.strength = strength
        self.rect = pg.Rect(pos, (18,18))

    def tick(self, render):
        # move
        self.x += self.spx*self.speed
        self.y += self.spy*self.speed
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        outofbounds = self.x>render.WIDTH or self.x<0 or self.y>render.HEIGHT or self.y<0
        if outofbounds:
            render.bullets.remove(self)
            return

        # collisions
        for enemy in render.enemies:
            if enemy.rect.colliderect(self.rect):
                enemy.damage(render, self.strength)

                # we are ded
                render.bullets.remove(self)
                return
        

    def draw(self, render):
        circle_renderer(render, self.rect, "yellow", radius=self.rect.width//2)