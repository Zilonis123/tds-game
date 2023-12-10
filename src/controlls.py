import pygame as pg
from .Entities.turrets import *
from .Entities.enemies import Enemy
from .Visuals.UI import UIe
from .sound import play

from loguru import logger


def mouse_down(render):
    render.mouseDown = render.mousePos
    
def mouse_up(render):
    clicked = _clean_click_check(render, render.UI)


    if clicked == None:
        # check if we have a turret in our hands
        clicked = False
        if render.actionRN == "grabturret":
            _place_turret(render)
        else:
            # check if we are clicking on a placed turret
            clicked = _click_turret(render)

            if not clicked:
                # check if we are clicking on an enemy
                clicked = _click_enemy(render)

        render.mouseDown = (-99, -99) # blank values

        if clicked:
            play(render, "Minimalist11.mp3")
        return
    
    play(render, "Minimalist11.mp3")
    render.mouseDown = (-99, -99) # blank values
    remove_delete_btn(render)
    clicked.action(render)    

def mouse_move(render, pos: tuple[float, float]):
    
    render.mousePos = pos
    # update hovered values on UI
    for e in render.UI: e.hovered = e.rect.collidepoint(pos)
    for e in render.turrets: e.hovered = e.rect.collidepoint(pos)

            
def _clean_click_check(render, objects: list):
    for e in objects:
        if e.rect.collidepoint(render.mouseDown):
            if e.rect.collidepoint(render.mousePos):
                return e
    return None

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
        if UI.type == "delete":
            render.UI.remove(UI)
            break

def _click_enemy(render):
   
    enemyClicked: None | Enemy = _clean_click_check(render, render.enemies)

    # select the enemy
    if enemyClicked != None and render.selectedEnemy == None:
        render.selectedEnemy = enemyClicked

        # calc size
        font = render.fonts.get("Gobold.otf-18")
        surface = font.render(f"Target {enemyClicked.targetTurret}", True, "black")

        # create delete button
        deleteBtn = UIe("changeTarget", enemyClicked.rect.topright, "clear", turretId=enemyClicked.targetTurret, size=surface.get_rect().size)

        render.UI.append(deleteBtn)

    elif render.actionRN != "changeTarget":
        render.selectedEnemy = None

    return enemyClicked != None

def _click_turret(render):
    # check if we have clicked on a turret
    clickedOn: None | Turret = _clean_click_check(render, render.turrets)
    
    if clickedOn == None:
        
        # deselect previous turret
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
            render.selectedTurret = None
            return True


    if render.actionRN == "changeTarget":
        # change enemy target
        if render.selectedEnemy != None:
            render.actionRN = None 
            render.selectedEnemy.change_target(clickedOn.uid)
            return True

   
    # select the turret
    render.actionRN = "selectTurret"

    # create the UI elements needed4
    rect: pg.Rect = clickedOn.rect
    pos: tuple[float, float] = (rect.x+rect.width, rect.y-rect.height//7) # calculate offset
    deleteBtn: UIe = UIe("delete", pos, "red", size=(30, 30))
    render.UI.append(deleteBtn)

    render.selectedTurret: Turret = clickedOn

    return True


def selectTurret(render, type):
    mx,my = render.mousePos

    ui = None
    for e in render.UI:
        if e.type == type:
            ui = e
            break
    
    if ui == None or ui.cost > render.cash or render.actionRN != None:
        return

    render.actionRN = "grabturret"
    render.selectedTurret = Turret(type, mx, my, render)

    render.addcash(-ui.cost)

