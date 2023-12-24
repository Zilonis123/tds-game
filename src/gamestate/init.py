from ..Visuals.renderers import *
from ..Visuals.UI import UIe
from ..usefulmath import changeTuple, remove_string
from ..sound import play_music
import os

def change_gamestate(render, to: str):

    # fadeout music
    play_music(render, None)
    
    if to == "game":
        render.UI: list[UIe] = [
            UIe(1, (10,5), "blue"),
            UIe(3, (10,185), "green", renderer=triangle_render),
            UIe(4, (10,277), "brown", renderer=hexagon_render),
            UIe(2, (10,92), "yellow")
        ]
    elif to == "mainmenu":
        def action(render):
            change_gamestate(render, "game")
        render.UI = [UIe("mainmenu", render.screencenter, "gray", size=(200, 50), align="center", action=action, text="START")]
        def action(render):
            change_gamestate(render, "controlls")

        render.UI.append(
            UIe("mainmenu", changeTuple(render.screencenter, (0, 70)), "gray", size=(200, 50), align="center", 
            action=action, text="CONTROLLS")
            )

        # play_music(render, "music/mainmenu-theme.mp3")
            
    elif to == "Loading":
        # generate thing to load
        render.FPS = 999
        render.notloaded = {"fonts":[], "imgs": [], "sounds": []}

        directory_path = os.path.join(render.dir, "assets/fonts")

        # fonts
        font_sizes = [i for i in range(15, 51)] # determines how many sizes we are going to load

        for filename in os.listdir(directory_path):
            # Check if the path is a file (not a directory)
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                for size in font_sizes:
                    render.notloaded["fonts"].append((filename, size))

        # imgs
        path = os.path.join(render.dir, "assets/imgs")
        find_unloaded(render, path, "imgs")

        directory_path = os.path.join(render.dir, "assets/sounds")

        for filename in os.listdir(directory_path):
            # Check if the path is a file (not a directory)
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                render.notloaded["sounds"].append(filename)
            else:
                # directory
                x = directory_path+f"/{filename}"
                n = filename
                for filename in os.listdir(x):
                    # Check if the path is a file (not a directory)
                    file_path = os.path.join(x, filename)
                    if os.path.isfile(file_path):
                        render.notloaded["sounds"].append(os.path.join(n, filename))

    elif to == "controlls":
        def action(render):
            change_gamestate(render, "mainmenu")

        render.UI = [
            UIe("mainmenu", (render.WIDTH, render.HEIGHT), "gray", size=(200, 50), align="bottomright", 
            action=action, text="Back")
        ]

    render.gamestate = to


def find_unloaded(render, path, type):
    for filename in os.listdir(path):
        # Check if the path is a file (not a directory)
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            render.notloaded[type].append(remove_string(path, os.path.join(render.dir, "assets/imgs"))+"/"+filename)
        else:
            find_unloaded(render, os.path.join(path, filename), type)