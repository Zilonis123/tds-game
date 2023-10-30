import pygame as pg
from ..Visuals.renderers import circle_renderer

class Bullet():
    def __init__(self, spx, spy, pos, strength, bulletSpeed, turret='none'):
        self.spx = spx
        self.spy = spy
        self.speed = bulletSpeed
        self.x, self.y = pos
        self.strength = strength
        self.rect = pg.Rect(pos, (18,18))

        self.turret = turret

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
                
                # increase turret stats
                if self.turret != "none":
                    self.turret.damagedealt += self.strength
                    # check if killed
                    if _find_enemy(render, enemy.uid) == "none":
                        self.turret.kills += 1
                return
        

    def draw(self, render):
        circle_renderer(render, self.rect, "yellow", radius=self.rect.width//2)


def _find_enemy(render, id):
    target = "none"
    for enemy in render.enemies:
        if enemy.uid != id:
            continue
        target = enemy.uid
    return target