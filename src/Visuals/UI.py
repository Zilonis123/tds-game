import pygame as pg
from ..usefulmath import translate_rect_to_circ, findenemy_by_id, adjust_color, changeTuple
from .renderers import square_render, text
from ..Entities.turrets import Turret
from random import uniform
import json

# UIe - UI element  
class UIe:
    def __init__(self, type: int|str, pos: tuple[int, int], color: str, renderer=square_render, size=(50,50), align="topleft", **info):

        self.pos = pos

        self.top = pos[0]
        self.left = pos[1]
        
        if align == "center":
            self.pos = changeTuple(self.pos, (-size[0]//2, size[1]//2))
        elif align == "bottomright":
            self.pos = changeTuple(self.pos, (-size[0], -size[1]))

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

        self.cost: int = 100 # default value

        # if shop then get info about me
        if self.isTurretspawn:
            f = open("info/turrets.json")
            data = json.load(f)
            data = data[str(type)] # get the data about ourselfes

            self.name = data["name"]
            self.description = data["description"]
            self.cost = data["cost"]

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
        elif self.type == "mainmenu":
            self.renderer(render, self.rect, dcolor, border=30)

            text(render, self.info["text"], "BLACK", self.rect.center, font="Nexa-Heavy.ttf")
       
            
        if self.hovered and self.type != "delete" and self.type != "mainmenu":
            self.renderer(render, self.rect, "white", width=2)

            if self.isTurretspawn:
                mx,my = render.mousePos
                OFFSET = 23
                y = my

                r = text(render, f"Name: {self.name}", "white", (mx+OFFSET, y), type="topleft",
                    font="VCR_MONO.ttf", background=True)
                y += r.height

                r = text(render, f"{self.cost}$", "white" if render.cash >= self.cost else "red", (mx+OFFSET, y), type="topleft",
                font="VCR_MONO.ttf", background=True)
                y += r.height

                text(render, f'"{self.description}"', "white", (mx+OFFSET, y), type="topleft",
                    font="VCR_MONO.ttf", background=True)

    def action(self, render):
        if self.isTurretspawn:
            if render.cash < self.cost:
                return
            # grab turret
            mx,my = render.mousePos

            render.actionRN = "grabturret"
            render.selectedTurret = Turret(self.type, mx, my, render)

            render.addcash(-self.cost)
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