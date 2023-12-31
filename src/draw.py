
import psutil,time
import pygame as pg
from .Visuals.renderers import text, square_render
from .usefulmath import changeTuple

def draw_game_background(render):
    color = [pg.Color(61,133,198), pg.Color(111,168,220)]
    sqsize = 75
    for x in range(render.WIDTH//sqsize+1):
        for y in range(render.HEIGHT//sqsize+1):
            r = pg.Rect((x*sqsize,y*sqsize), (sqsize, sqsize))
            pg.draw.rect(render.screen, color[(y+x%2)%2], r)

def draw_UI(render):
    bRect = pg.Rect((0,0), (80, render.HEIGHT))
    pg.draw.rect(render.screen, "beige", bRect)
    pg.draw.rect(render.screen, pg.Color(206,126,0), bRect, 4)

    for UIe in render.UI:
        UIe.draw(render)

    # draw text
    text(render, str(render.cash), "BLACK", (render.WIDTH, 0), size=30, type="topright", font="Gobold.otf")

    # draw grid lines if SHIFT pressed
    keys = pg.key.get_pressed()
    if keys[pg.K_LSHIFT]:
        draw_grid(render)

    if render.speedUp:
        text(render, "2x", "white", (render.WIDTH//2, 20), size=25, background=True, font="VCR_MONO.ttf")


def draw_grid(render):
    # draw horizonatally
    for i in range(render.WIDTH//render.gridsize+1):
        pg.draw.line(render.screen, "white", (i*render.gridsize, 0), (i*render.gridsize, render.HEIGHT))

    # draw vertically
    for i in range(render.HEIGHT//render.gridsize+1):
        pg.draw.line(render.screen, "white", (0, i*render.gridsize), (render.WIDTH, i*render.gridsize))

def draw_turrets(render):

    for turret in render.turrets:
        if render.selectedTurret == turret:
            continue
        turret.draw(render)

    # draw selected turret 1st
    if render.selectedTurret != None:
        render.selectedTurret.draw(render)

    
    # draw current in hand
    if render.actionRN == "grabturret":

        # change color depending if the turret can be placed
        rectColor = render.selectedTurret.color
        for turret in render.turrets:
            if turret.plzone.colliderect(render.selectedTurret.rect):
                rectColor = "red"
                break

        render.selectedTurret.draw(render, rectColor)

def draw_debug(render):

    y=0

    rect = text(render, f"FPS {round(render.FPSGraph[-1])} (AVG {round(sum(render.FPSGraph)/len(render.FPSGraph))})", 
    "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")
    y+=rect.height

    rect = text(render, f"{render.count_entities()} entities", 
    "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")
    y+=rect.height

    rect = text(render, f"Running for {round(time.time()-render.startTime, 1)}s", "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")
    y+=rect.height

    rect = text(render, f"Fonts loaded {len(render.fonts)}"
    , "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")

    y+=rect.height

    rect = text(render, f"Imgs loaded {len(render.imgs)}"
    , "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")

    # FPS Graph
    location = (100, render.HEIGHT-10)

    size = 2 # how big is the graph

    points: list[tuple[float, float]] = []

    for i in range(len(render.FPSGraph)):
        val: int = render.FPSGraph[i]
        point: tuple[float, float] = (location[0]+i*size, location[1]-val*size)

        if i-1>=0 and val == render.FPSGraph[i-1]:
            points.pop()

        points.append(point)
    
    if len(points) > 2:
        pg.draw.lines(render.screen, "red", False, points, width=3)

        ADJUSTED_FPS = render.FPS+3
        r = pg.Rect((location[0], location[1]-ADJUSTED_FPS*size), (len(render.FPSGraph)*size, ADJUSTED_FPS*size))
        square_render(render, r, "white", width=2)
        text(render, "FPS", "WHITE", r.midtop, background=True)

        for i in range(render.FPS+2):
            if i%10 == 0:
                text(render, str(i), "white", (r.bottomleft[0], location[1]-i*size), type="bottomright", background=True,
                size=5*size)

def blurScreen(render):
    square_render(render, pg.Rect((0,0), (render.WIDTH, render.HEIGHT)), pg.Color(255, 255, 255, 75))



