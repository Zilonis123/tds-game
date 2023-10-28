import pygame as pg
from .turrets import *

def mouse_click(render):
    mx,my = pg.mouse.get_pos()

    # Check if mouse was clicked on a UI element
    # and that we dont already have a turret in our hands
    t = _check_UI(render, mx,my)
    if not t and not render.actionRN == "grabturret":
        return
    
    # If we have a turret selected -
    if render.actionRN == "grabturret":

        # check if turret collides with any existing turret
        for turret in render.turrets:
            if turret.plzone.colliderect(render.handturret.rect):
                return
        # else - "build" the turret

        addTurret(render, render.handturret)
        render.actionRN = "none"
        return
    # else - select a turret

    render.actionRN = "grabturret"
    render.handturret = Turret(t, mx, my)

def _check_UI(render, mx,my):
    # checks if the the given pos is over a "button"

    for UIe in render.UI:
        if UIe.rect.collidepoint(mx, my):
            return UIe.type
    return False