import pygame as pg

class Turret():
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.pos = (x,y)

        self.rect = pg.Rect(self.pos, (50, 50))
        self.plzone = pg.Rect((x-10,y-10), (70, 70)) # zone where no turret can be placed

        if type == 1:
            self.color = "orange"
        elif type == 2:
            self.color = "green"

def addTurret(renderer, t):
    renderer.turrets.append(t)