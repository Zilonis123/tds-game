# this file will have a bunch of functions that will change how
# a turret or UIe looks

import pygame as pg

def triangle_render(render, rect, color, isOutline=0):
    x=rect.x
    y=rect.y
    w=rect.width
    h=rect.height

    vertixes = [(x+w//2,y), (x,y+h), (x+w,y+h)]

    # draw
    pg.draw.polygon(render.screen, color, vertixes, isOutline)

def square_render(render, rect, color, isOutline=0):
    pg.draw.rect(render.screen, color, rect, isOutline)