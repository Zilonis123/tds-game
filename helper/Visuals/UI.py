import pygame as pg
from ..usefulmath import translate_rect_to_circ, findenemy_by_id
from .renderers import square_render, text
from ..Entities.turrets import Turret

# UIe - UI element
class UIe:
    def __init__(self, type: int|str, pos: tuple[int, int], color: str, renderer=square_render, size=(50,50), info={}):

        # info var contains stuff that the UI element should know

        self.pos = pos
        if color.lower() == "clear":
            color = pg.Color(0,0,0,0)

        self.color: pg.Color = pg.Color(color) # Use pygame Color because its better
        self.top: int = pos[0]
        self.left: int = pos[1]

        self.info = info

        self.isTurretspawn: bool = isinstance(type, int)
        self.type: int = type
        self.rect: pg.Rect = pg.Rect(pos, size)
        self.renderer = renderer

        self.cost: int = 100

        # delete logic
        if self.type == "delete":

            # "Hitbox"
            self.rect = pg.Rect(pos, (30,30))
            self.rect: pg.Rect = pg.Rect(translate_rect_to_circ(self.rect), (self.rect.w, self.rect.h))

    def draw(self, render):
        if self.type == "delete":
            pg.draw.circle(render.screen, self.color, self.pos, 15) # draw circle
            pg.draw.circle(render.screen, "black", self.pos, 15, 2) # draw outline
            # draw a X
            # self.pos - circle center
            pg.draw.line(render.screen, "white", (self.top+8, self.left+8), (self.top-8, self.left-8), 3)
            pg.draw.line(render.screen, "white", (self.top-8, self.left+8), (self.top+8, self.left-8), 3)
        else:
            self.renderer(render, self.rect, self.color)
            color = "GREEN"
            if render.cash < self.cost:
                color = "RED"
            
            text(render, str(self.cost), color, (self.rect.centerx, self.rect.centery+(self.rect.h//3*2)),
             font="fonts/Gobold.otf")
            

    def action(self, render):
        if self.isTurretspawn:
            if render.cash < self.cost:
                return
            # grab turret
            mx,my = pg.mouse.get_pos()

            render.actionRN = "grabturret"
            render.selectedTurret = Turret(self.type, mx, my, render)

            render.cash -= self.cost
            render.ttext.append({"cash": -self.cost, "time": 0})
        elif self.type == "delete":
            render.turrets.remove(render.selectedTurret)
            render.UI.remove(self)
            render.actionRN = None
            render.selectedTurret = None
        elif self.type == "changeTarget":
            e = findenemy_by_id(render, self.info["id"])
            render.enemies.remove(e)
            render.selectedEnemy = None
    
    def tick(self, render):
        if self.type == "changeTarget":

            e = findenemy_by_id(render, self.info["id"])
            if e != None and render.selectedEnemy == e: 
                self.rect.topleft = e.rect.topright
            else:
                render.UI.remove(self)