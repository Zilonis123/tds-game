
import os
import pygame as pg
from ..Entities.turrets import Turret
from .init import change_gamestate
from src.wavehandler import *


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


    if is_wave_finished(render):
        render.wave += 1
        start_next_wave(render)

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
        f: tuple[str, int] = render.notloaded["fonts"].pop()
        file_path = os.path.join(render.dir+"/assets/fonts", f[0])
        if os.path.isfile(file_path):
            font = pg.font.Font(file_path, f[1])
            render.fonts[f[0]+f"-{f[1]}"] = font
            
    if len(render.notloaded["imgs"]) > 0:
        i: str = render.notloaded["imgs"].pop()
        file_path = f"{render.dir}/assets/imgs/{i}"
        if os.path.isfile(file_path):
            img = pg.image.load(file_path).convert_alpha()
            render.imgs[i] = img

    if len(render.notloaded["sounds"]) > 0:
        i: str = render.notloaded["sounds"].pop()
        file_path = f"{render.dir}/assets/sounds/{i}"
        if not pg.mixer.get_init():
            pg.mixer.init()
        sfx = pg.mixer.Sound(file_path)
        render.sounds[i] = sfx

    if sum(len(lst) for lst in render.notloaded.values()) <= 0:
        change_gamestate(render, "mainmenu")
