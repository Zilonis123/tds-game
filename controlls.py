import pygame as pg
from turrets import *

def mouse_click(render):
    mx,my = pg.mouse.get_pos()

    r = pg.Rect(10,10,50,50)

    if not r.collidepoint(mx,my) and not render.actionRN == "grabturret":
        return
    
    if render.actionRN == "grabturret":

        # check if turret collides with any existing turret
        for turret in render.turrets:
            if turret.plzone.colliderect(render.handturret.rect):
                return

        turret = Turret(1, mx, my)

        addTurret(render, turret)
        render.actionRN = "none"
        return

    render.actionRN = "grabturret"
    render.handturret = Turret(1, mx, my)