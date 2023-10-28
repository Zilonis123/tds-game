import pygame as pg

class UIe:
    def __init__(self, type, pos, color, turret="none"):
        self.pos = pos
        self.color = color

        self.isTurretspawn = isinstance(type, int)
        self.type = type
        self.rect = pg.Rect(pos, (50,50))

        # delete logic
        self.turret = turret
    def draw(self, render):
        pg.draw.rect(render.screen, self.color, self.rect)

    def action(self, render):
        if self.type == "delete":
            render.turrets.remove(self.turret)
            render.UI.remove(self)