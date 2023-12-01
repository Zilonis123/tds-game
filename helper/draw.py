
import psutil,time
import pygame as pg
from .Visuals.renderers import text, square_render


def draw_UI(render):
    bRect = pg.Rect((0,0), (80, render.HEIGHT))
    pg.draw.rect(render.screen, "beige", bRect)
    pg.draw.rect(render.screen, pg.Color(206,126,0), bRect, 4)

    for UIe in render.UI:
        UIe.draw(render)

    # draw text
    text(render, str(render.cash), "BLACK", (render.WIDTH, 0), size=30, type="topright", font="fonts/Gobold.otf")

    # draw grid lines if SHIFT pressed
    keys = pg.key.get_pressed()
    if keys[pg.K_LSHIFT]:
        draw_grid(render)


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

    # memory
    if render.ticks%240 or not render.cache["memory"]:
        size = psutil.Process().memory_info().rss
        store = round(size/1024**2)
        render.cache["memory"] = store

    mem = render.cache["memory"]

    y=0
    rect = text(render, f"Memory {mem}Kb", "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")
    y+=rect.height

    rect = text(render, f"FPS {round(render.clock.get_fps())}", "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")
    y+=rect.height

    rect = text(render, f"{render.count_entities()} entities", 
    "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")
    y+=rect.height

    rect = text(render, f"Running for {round(time.time()-render.startTime, 1)}s", "white", (render.WIDTH, render.HEIGHT-y), background=True, type="bottomright")
    y+=rect.height

    rect = text(render, f"Fonts loaded {len(render.fonts)}"
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

        square_render(render, pg.Rect((location[0], location[1]-63*size), (len(render.FPSGraph)*size, 63*size)), "white", width=2)


def blurScreen(render):
    square_render(self, pg.Rect((0,0), (self.WIDTH, self.HEIGHT)), pg.Color(255, 255, 255, 75))
