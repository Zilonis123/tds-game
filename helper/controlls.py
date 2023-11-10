import pygame as pg
from .Entities.turrets import *
from .Entities.enemies import Enemy
from .Visuals.UI import UIe

from loguru import logger

def mouse_click(render):
    mx,my = pg.mouse.get_pos()


    # Check if mouse was clicked on a UI element and not action is done right now
    clickedOnUI: bool = click_UI(render, mx,my)

    if not clickedOnUI:
        # check if we have a turret in our hands
        if render.actionRN == "grabturret":
            _place_turret(render)
        else:
            # check if we are clicking on a placed turret
            _click_turret(render, mx, my)

            # check if we are clicking on an enemy
            click_enemy(render, mx, my)
    

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
        if UI.type == "delete":
            render.UI.remove(UI)
            break

def click_enemy(render, mx: float, my: float):
    enemyClicked: None | Enemy = None
    
    for e in render.enemies:
        if e.rect.collidepoint(mx, my):
            enemyClicked = e
            break

    # select the enemy :0
    if enemyClicked != None and render.selectedEnemy == None:
        render.selectedEnemy = enemyClicked

        # calc size
        font = pg.font.Font("fonts/Gobold.otf", 18)
        surface = font.render(f"Target {enemyClicked.targetTurret}", True, "black")

        render.UI.append(UIe("changeTarget", enemyClicked.rect.topright, "clear", info={"id": e.uid}, size=surface.get_rect().size))

        logger.info(f"Created UI: {len(render.UI)}")
    elif render.actionRN != "changeTarget":
        render.selectedEnemy = None

def _click_turret(render, mx, my):
    # check if we have clicked on a turret
    clickedOn: None | Turret = None
    for turret in render.turrets:
        if turret.rect.collidepoint(mx, my):
            clickedOn = turret
            break
    
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
            return


    if render.actionRN == "changeTarget":
        # change enemy target
        if render.selectedEnemy != None:
            render.actionRN = None 
            render.selectedEnemy.change_target(clickedOn.uid)
            return

   
    # select the turret
    render.actionRN = "selectTurret"

    # create the UI elements needed4
    rect: pg.Rect = clickedOn.rect
    pos: tuple[float, float] = (rect.x+rect.width, rect.y-rect.height//7) # calculate offset
    deleteBtn: UIe = UIe("delete", pos, "red")
    render.UI.append(deleteBtn)

    render.selectedTurret: Turret = clickedOn

    logger.info(f"Created UI: {len(render.UI)}")
