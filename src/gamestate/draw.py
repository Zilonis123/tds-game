from ..draw import *
from ..Visuals.renderers import image


# game state draw funcs
def draw_game(render):
    render.screen.fill("darkgray")

    
    draw_turrets(render)

    # bullets
    for b in render.bullets: b.draw(render)

    # draw enemies
    for e in render.enemies: e.draw(render)
    for e in render.enemies: e.draw_after(render) # We do this so that enemies dont cover things like health


    draw_UI(render)

    for t in render.ttext:
        t.draw(render)
        t.func(t, render)

    if render.actionRN == "changeTarget":

        # this creates a blur effect
        blurScreen(render)

        text(render, "Change Target", "black", (render.WIDTH, render.HEIGHT), type="bottomright", 
        font="Gobold.otf", background=True)



def draw_loading(render):
    def draw_bar(render, type: str, tt: str, y: int):
        hsize = 300 # half of the line
        center = render.screencenter

        length: int = round((len(render.notloaded[type])/(len(render.notloaded[type])+len(render.fonts)))*(hsize*2))

        
        pg.draw.line(render.screen, "gray", (center[0]-hsize, y), (center[0]+hsize, y), 50)
        pg.draw.line(render.screen, "green", (center[0]-hsize, y), ((center[0]-hsize)+length, y), 50)

        t = f"Loaded {len(render.notloaded[type])}/{len(render.notloaded[type])+len(render.fonts)} {tt}"

        text(render, t, "white", (center[0], y))


    render.screen.fill("black")

    
    


    if len(render.notloaded["fonts"]) > 0:
        draw_bar(render, "fonts", "fonts", render.HEIGHT-70)
    
    if len(render.notloaded["imgs"]) > 0:
        draw_bar(render, "imgs", "images", render.HEIGHT-130)

    if len(render.notloaded["sounds"]) > 0:
        draw_bar(render, "sounds", "sounds", render.HEIGHT-190)

def draw_mainmenu(render):
    render.screen.fill("lightblue")

    text(render, "Some Tower Defense", "black", changeTuple(render.screencenter, (0, -90)), size=46, font="Nexa-Heavy.ttf")

    for e in render.UI: e.draw(render)

def draw_controlls(render):
    render.screen.fill("lightblue")

    for e in render.UI: e.draw(render)


    controlls = [("/keyboard_light/Alt_Key_Light.png", "Run the game at 2x speed"), ("/keyboard_light/Ctrl_Key_Light.png", "Opens the debug menu")
    ,("/keyboard_light/Space_Key_Light.png", "Kills all the enemies")]

    y = 0
    for c in controlls:
        img,desc = c
        img = pg.transform.scale(render.imgs[img], (50, 50))
        image(render, img, (0, y))
        text(render, desc, "black", (50, y), font="Nexa-ExtraLight.ttf", size=15, type="topleft")
        y += 50
        