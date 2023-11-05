import pygame as pg
from .Entities.turrets import *
from .Visuals.UI import UIe

def mouse_click(render):
    mx,my = pg.mouse.get_pos()


    # Check if mouse was clicked on a UI element and not action is done right now
    res: bool = click_UI(render, mx,my)

    if res == False:
        # check if we have a turret in our hands
        if render.actionRN == "grabturret":
            _place_turret(render)
        else:
            # check if we are clicking on a placed turret
            _click_turret(render, mx, my)
    

def click_UI(render, mx: float|int ,my: float|int):
    # checks if the the given pos is over a "button"

    for UIe in render.UI:
        if UIe.rect.collidepoint(mx, my):

            # press it
            remove_delete_btn(render)
            UIe.action(render)
            return True


    # no ui was clicked
    return False

def _place_turret(render):
    # check if turret collides with any existing turret
    for turret in render.turrets:
        if turret.plzone.colliderect(render.selectedTurret.rect):
            return
    # else - place the turret

    addTurret(render, render.selectedTurret)
    render.actionRN = None
    
    # remove selected turret
    render.selectedTurret = None
    return

def remove_delete_btn(render):
    # function to remove delete button
    for UI in render.UI:
        if UI.turret == render.selectedTurret:
            render.UI.remove(UI)

def _click_turret(render, mx, my):
    # check if we have clicked on a turret
    clickedOn: None | Turret = None
    for turret in render.turrets:
        if turret.rect.collidepoint(mx, my):
            clickedOn = turret 
    
    if clickedOn == None:
        # if we have something selected deselect it
        if render.actionRN == "selectTurret":
            remove_delete_btn(render)
            render.actionRN = None
            # remove selected turret
            render.selectedTurret: Turret = Turret(1, -999, -999, render)
        return
    
    # deselect current turret and select another one
    if render.actionRN == "selectTurret":

        # remove delete button
        remove_delete_btn(render)

        # if we are trying to select the same turrent .. dont allow it
        if clickedOn == render.selectedTurret:
            render.actionRN = None
            render.selectedTurret = Turret(1, -999, -999, render)
            return

   
    # select the turret
    render.actionRN = "selectTurret"

    # create the UI elements needed4
    rect: pg.Rect = clickedOn.rect
    pos: tuple[float, float] = (rect.x+rect.width, rect.y-rect.height//7) # calculate offset
    deleteBtn: UIe = UIe("delete", pos, "red", clickedOn)
    render.UI.append(deleteBtn)

    render.selectedTurret: Turret = clickedOn