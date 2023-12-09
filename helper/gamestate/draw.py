from ..draw import *


# game state draw funcs
def draw_game(render):
    render.screen.fill("darkgray")

    # draw enemies
    for e in render.enemies: e.draw(render)

    draw_turrets(render)

    # bullets
    for b in render.bullets: b.draw(render)

    draw_UI(render)

    for t in render.ttext:
        prefix = "+"
        color = "green"
        if t["cash"] < 0:
            prefix=""
            color = "red"

        text(render, prefix+str(t["cash"]), color, (render.WIDTH, 50+t["time"]), type="topright")
        t["time"] += 1
        if t["time"] > 120:
            render.ttext.remove(t)

    if render.actionRN == "changeTarget":

        # this creates a blur effect
        blurScreen(render)

        text(render, "Change Target", "black", (render.WIDTH, render.HEIGHT), type="bottomright", 
        font="fonts/Gobold.otf", background=True)

    if render.debug:
        draw_debug(render)

def draw_loading(render):
    render.screen.fill("black")

    center = render.screencenter
    hsize = 300 # half of the line

    pg.draw.line(render.screen, "gray", (center[0]-hsize, center[1]), (center[0]+hsize, center[1]), 50)

    length: int = round((len(render.notloaded["fonts"])/(len(render.notloaded["fonts"])+len(render.fonts)))*(hsize*2))
    pg.draw.line(render.screen, "green", (center[0]-hsize, center[1]), ((center[0]-hsize)+length, center[1]), 50)


    text(render, f"loaded {len(render.notloaded['fonts'])}/{len(render.notloaded['fonts'])+len(render.fonts)} fonts", "white", center)

def draw_mainmenu(render):
    render.screen.fill("lightblue")

    text(render, "Some Tower Defense", "black", changeTuple(render.screencenter, (0, -90)), size=46, font="Nexa-Heavy.ttf")

    for e in render.UI: e.draw(render)