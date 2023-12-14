import pygame as pg
from ..Visuals.renderers import circle_renderer
from ..sound import play
from dataclasses import dataclass

@dataclass
class Bullet():
    spx: int
    spy: int
    pos: tuple[int, int]
    strength: float | int
    speed: float

    def __post_init__(self):
        self.x, self.y = self.pos
        self.rect = pg.Rect(self.pos, (18,18))

        self.playedFire = False

    def tick(self, render):
        if self.playedFire == False:
            play(render, "Shoot.wav")
            self.playedFire = True

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

                render.bullets.remove(self)
                return
        

    def draw(self, render):
        circle_renderer(render, self.rect, "yellow", radius=self.rect.width//2)