import pygame as pg
from .Entities.turrets import *
from .Visuals.UI import UIe

def mouse_click(render):
    mx,my = pg.mouse.get_pos()


    # Check if mouse was clicked on a UI element and not action is done right now
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
            canPlaceTurret = render.actionRN == "none" or render.actionRN == "grabTurret"
            if UIe.isTurretspawn and canPlaceTurret:
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
            if turret.plzone.colliderect(render.selectedTurret.rect):
                return
        # else - "build" the turret

        addTurret(render, render.selectedTurret)
        render.actionRN = "none"
        # remove selected turret
        render.selectedTurret = Turret(1, -999, -999, render)
        return
    # else - select a turret

    render.actionRN = "grabturret"
    render.selectedTurret = Turret(type, mx, my, render)

def _click_turret(render, mx, my):
    def remove_delete_btn(render):
        # function to remove delete button
        for UI in render.UI:
            if UI.turret == render.selectedTurret:
                render.UI.remove(UI)

    # check if we have clicked on a turret
    clickedOn = "none"
    for turret in render.turrets:
        if turret.rect.collidepoint(mx, my):
            clickedOn = turret 
    
    if clickedOn == "none":
        # if we have something selected deselect it
        if render.actionRN == "selectTurret":
            remove_delete_btn(render)
            render.actionRN = "none"
            # remove selected turret
            render.selectedTurret = Turret(1, -999, -999, render)
        return
    
    # deselect current turret and select another one
    if render.actionRN == "selectTurret":

        # remove delete button
        remove_delete_btn(render)

        # if we are trying to select the same turrent .. dont allow it
        if clickedOn == render.selectedTurret:
            render.actionRN = "none"
            render.selectedTurret = Turret(1, -999, -999, render)
            return

   
    # select the turret
    render.actionRN = "selectTurret"

    # create the UI elements needed4
    rect = clickedOn.rect
    pos = (rect.x+rect.width, rect.y-rect.height//7) # calculate offset
    deleteBtn = UIe("delete", pos, "red", clickedOn)
    render.UI.append(deleteBtn)

    render.selectedTurret = clickedOn