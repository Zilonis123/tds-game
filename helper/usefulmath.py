# this file will contain anything to make the code more readable
import math
import pygame as pg

def translate_rect_to_circ(rect):
    # converts rects pos to match a circles pos -- moves rect to its center
    return (rect.x-rect.width//2, rect.y-rect.height//2)


def diagonally_pathfind(b, a):
    dx = round(a[0] - b[0])
    dy = round(a[1] - b[1])

    magnitude = math.sqrt(dx**2 + dy**2)

    if 2 > magnitude < 2:
        direction = (0, 0)
    else:
        direction = ((dx / magnitude), (dy / magnitude))
    
    return direction

def adjust_color(color, adjustment):
    # makes a color lighter or darker

    # check if color is pygame color
    if not isinstance(color, pg.Color):
        color = pg.Color(color)

    r = color.r
    g = color.g
    b = color.b
    r = max(0, min(255, r + adjustment))
    g = max(0, min(255, g + adjustment))
    b = max(0, min(255, b + adjustment))
    return (r, g, b)

def pointInCircle(p1, circleCenter, radius):
    d = math.sqrt((p1[0] - circleCenter[0])**2+(p1[1] - circleCenter[1]) ** 2)
    return d <= radius