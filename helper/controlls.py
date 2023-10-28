import pygame as pg
from .turrets import *
from .UI import UIe

def mouse_click(render):
    mx,my = pg.mouse.get_pos()

    # Check if mouse was clicked on a UI element
    res = _check_UI(render, mx,my)

    if res == False:
        # check if we have a turret in our hands
        if render.actionRN == "grabturret":
            _grab_turret(render)
        else:
            # check if we are clicking on a placed turret
            _click_turret(render, mx, my)
    

def _check_UI(render, mx,my):
    # checks if the the given pos is over a "button"

    for UIe in render.UI:
        if UIe.rect.collidepoint(mx, my):
            if UIe.isTurretspawn:
                # if UI element is a turretspawn .. make a turret
                _grab_turret(render, UIe.type)
                return
            else:
                UIe.action(render)
                return

    # no ui was clicked
    return False

def _grab_turret(render, type="none"):

    mx,my = pg.mouse.get_pos()

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
    render.handturret = Turret(type, mx, my)

def _click_turret(render, mx, my):
    # check if we have clicked on a turret
    clickedOn = "none"
    for turret in render.turrets:
        if turret.rect.collidepoint(mx, my):
            clickedOn = turret 
    
    if clickedOn == "none" and not render.actionRN == "selectTurret":
        return
    
    # check if we are trying to deselect a turret
    if render.actionRN == "selectTurret" and clickedOn != "none":
        render.actionRN = "none"
        return
   
    # select the turret
    render.actionRN = "selectTurret"

    # create the UI elements needed
    deleteBtn = UIe("delete", (clickedOn.x+50, clickedOn.y-40), "red", clickedOn)
    render.UI.append(deleteBtn)