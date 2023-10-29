import pygame as pg
from ..Visuals.renderers import circle_renderer

class Bullet():
    def __init__(self, spx, spy, pos, strength):
        self.spx = spx
        self.spy = spy
        self.x, self.y = pos
        self.strength = strength
        self.rect = pg.Rect(pos, (18,18))

    def tick(self, render):
        # move
        self.x += self.spx/5
        self.y += self.spy/5
        self.rect = self.rect.move(round(self.x), round(self.y))
        print(self.x)

        
        
        # collisions
        for enemy in render.enemies:
            if enemy.rect.colliderect(self.rect):
                enemy.damage(render, self.strength)

                # we are ded
                render.bullets.remove(self)
                return
        

    def draw(self, render):
        circle_renderer(render, self.rect, "yellow", radius=self.rect.width//2)