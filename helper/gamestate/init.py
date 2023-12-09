from ..Visuals.renderers import *
from ..Visuals.UI import UIe


def change_gamestate(render, to: str):
    
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
        render.UI = [UIe("mainmenu-start", render.screencenter, "gray", size=(200, 50), align="center", action=action)]



    render.gamestate = to