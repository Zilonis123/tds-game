
import os
import pygame as pg
from ..Entities.turrets import Turret
from .init import change_gamestate


def run_game(render):
    # Tick
    if render.speedUp:
        for enemy in render.enemies:enemy.tick(render)
        for u in render.UI: u.tick(render)
        for turret in render.turrets:turret.tick(render)
        for b in render.bullets:b.tick(render)

    for enemy in render.enemies:enemy.tick(render)
    for u in render.UI: u.tick(render)
    for turret in render.turrets:turret.tick(render)
    for b in render.bullets:b.tick(render)

    mx,my = render.mousePos
    keys = pg.key.get_pressed()

    # if turret in hand update render.selectedTurret
    if render.actionRN == "grabturret":
        t = render.selectedTurret.type
        
        # if grid lines enabled
        if keys[pg.K_LSHIFT]:
            # snap to grid
            mx=mx+50/2
            my=my+50/2
            mx=round(mx/70)*render.gridsize
            my=round(my/70)*render.gridsize
            mx=mx-50-(render.gridsize-50)//2
            my=my-50-(render.gridsize-50)//2
        else:
            mx,my = (mx-render.selectedTurret.rect.w//2, my-render.selectedTurret.rect.h//2)
        render.selectedTurret = Turret(t, mx, my, render)




def run_loading(render):

    if len(render.notloaded["fonts"]) > 0:

        if len(render.notloaded["fonts"]) > 0:
            f: tuple[str, int] = render.notloaded["fonts"].pop()
            file_path = os.path.join(render.dir+"/assets/fonts", f[0])
            if os.path.isfile(file_path):
                font = pg.font.Font(file_path, f[1])
                render.fonts[f[0]+f"-{f[1]}"] = font
            
    elif len(render.notloaded["imgs"]) > 0:
        i: str = render.notloaded["imgs"].pop()
        file_path = f"{render.dir}/assets/imgs/{i}"
        if os.path.isfile(file_path):
            img = pg.image.load(file_path).convert_alpha()
            render.imgs[i] = img
    else:
        change_gamestate(render, "mainmenu")
