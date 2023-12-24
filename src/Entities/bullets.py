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
            # play(render, "Shoot.wav")
            self.playedFire = True

        # move
        self.x += self.spx*self.speed
        self.y += self.spy*self.speed
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

        rect = pg.Rect(-50,-50,render.WIDTH+100, render.HEIGHT+100)
        outofbounds = not rect.collidepoint(self.x, self.y)
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