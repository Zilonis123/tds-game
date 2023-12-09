import pygame as pg
from ..usefulmath import translate_rect_to_circ, findenemy_by_id, adjust_color, changeTuple
from .renderers import square_render, text
from ..Entities.turrets import Turret
from random import uniform

# UIe - UI element  
class UIe:
    def __init__(self, type: int|str, pos: tuple[int, int], color: str, renderer=square_render, size=(50,50), align="topleft", **info):

        self.pos = pos
        
        if align == "center":
            self.pos = changeTuple(self.pos, (-size[0]//2, size[1]//2))

        if color.lower() == "clear":
            color = pg.Color(0,0,0,0)

        self.color: pg.Color = pg.Color(color) # Use pygame Color because its better
        


        self.info = info

        self.hovered: bool = False # is the mouse over the UIe

        self.isTurretspawn: bool = isinstance(type, int)
        self.type: int = type
        self.rect: pg.Rect = pg.Rect(self.pos, size)
        self.renderer = renderer

        self.uid: str = str(int(uniform(1, 10000)))+str(self.type)

        self.cost: int = 100

        # delete logic
        if self.type == "delete":
            self.rect: pg.Rect = pg.Rect(translate_rect_to_circ(self.rect), (self.rect.w, self.rect.h))

        # if provided with a different action script .. use that
        if info.get("action", None) != None:
            self.action = info.get("action")

    def draw(self, render):
        dcolor = self.color
        if self.hovered == True:
            dcolor: pg.Color = adjust_color(dcolor, -45)

        if self.type == "delete":
            pg.draw.circle(render.screen, dcolor, self.pos, 15) # draw circle
            pg.draw.circle(render.screen, "black", self.pos, 15, 2) # draw outline
            # draw a X
            # self.pos - circle center
            pg.draw.line(render.screen, "white", (self.top+8, self.left+8), (self.top-8, self.left-8), 3)
            pg.draw.line(render.screen, "white", (self.top-8, self.left+8), (self.top+8, self.left-8), 3)
        elif self.isTurretspawn:
            self.renderer(render, self.rect, dcolor)
            color = "BLACK"
            if render.cash < self.cost:
                color = "RED"
            
            text(render, str(self.cost), color, (self.rect.centerx, self.rect.bottom+12), type="center",
             font="fonts/Gobold.otf")
        elif self.type == "mainmenu-start":
            self.renderer(render, self.rect, dcolor)

            text(render, "START", "BLACK", self.rect.center, font="fonts/Gobold.otf")
            
        if render.debug:
            text(render, str(self.hovered), "GREEN", self.rect.center, background=True, backgroundClr=pg.Color(0,0,0,75))

        if self.hovered and self.type != "delete":
            self.renderer(render, self.rect, "white", width=2)
        

    def action(self, render):
        if self.isTurretspawn:
            if render.cash < self.cost:
                return
            # grab turret
            mx,my = render.mousePos

            render.actionRN = "grabturret"
            render.selectedTurret = Turret(self.type, mx, my, render)

            render.cash -= self.cost
            render.ttext.append({"cash": -self.cost, "time": 0})
        elif self.type == "delete":
            render.turrets.remove(render.selectedTurret)

            for ui in render.UI:
                if ui.uid == self.uid:
                    render.UI.remove(ui)
            render.actionRN = None
            render.selectedTurret = None
        elif self.type == "changeTarget":
            render.actionRN = "changeTarget"
    
    def tick(self, render):
        if self.type == "changeTarget":

            e = findenemy_by_id(render, self.info["turretId"])
            if e != None and render.selectedEnemy == e: 
                self.rect.topleft = e.rect.topright
            else:
                render.UI.remove(self)

    # def __eq__(self, other):
    #     if isinstance(other, UIe):
    #         return self == other
    #     return False