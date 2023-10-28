import pygame as pg

class UIe:
    def __init__(self, type, pos, color):
        self.pos = pos
        self.color = color
        self.type = type
        self.rect = pg.Rect(pos, (50,50))

    def draw(self, render):
        pg.draw.rect(render.screen, self.color, self.rect)