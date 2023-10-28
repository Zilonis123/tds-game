import pygame as pg

class Turret():
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y
        self.pos = (x,y)
        self.size = (50,50) # may be subject to change

        self.rect = pg.Rect(self.pos, (50, 50))
        self.plzone = pg.Rect((x-10,y-10), (70, 70)) # zone where no turret can be placed

        if type == 1:
            self.color = "blue"
        elif type == 2:
            self.color = "yellow"
    
    def draw(self, render, color="none"):
        if color == "none":
            color = self.color
        pg.draw.rect(render.screen, color, self.rect)

def addTurret(renderer, t):
    renderer.turrets.append(t)
