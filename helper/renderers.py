# this file will have a bunch of functions that will change how
# a turret or UIe looks

import pygame as pg
import math

def triangle_render(render, rect, color, isOutline=0):
    x=rect.x
    y=rect.y
    w=rect.width
    h=rect.height

    vertexes = [(x+w//2,y), (x,y+h), (x+w,y+h)]

    # draw
    pg.draw.polygon(render.screen, color, vertexes, isOutline)

def square_render(render, rect, color, isOutline=0):
    pg.draw.rect(render.screen, color, rect, isOutline)

def hexagon_render(render, rect, color, isOutline=0):
    x,y=rect.center
    size = rect.width / math.sqrt(3)

    # future me. I am very sorry for this code you dont understand
    angle_deg = 360 / 6
    vertices = []
    for i in range(6):
        angle_rad = math.radians(angle_deg * i)
        hexagon_x = x + size * math.cos(angle_rad)
        hexagon_y = y + size * math.sin(angle_rad)
        vertices.append((hexagon_x, hexagon_y))

    pg.draw.polygon(render.screen, color, vertices, isOutline)