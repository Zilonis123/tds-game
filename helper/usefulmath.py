# this file will contain anything to make the code more readable
import math
import pygame

def translate_rect_to_circ(rect):
    # converts rects pos to match a circles pos -- moves rect to its center
    return (rect.x-rect.width//2, rect.y-rect.height//2)


def diagonally_pathfind(b, a):
    dx = a[0] - b[0]
    dy = a[1] - b[1]

    dx = round(dx)
    dy = round(dy)

    magnitude = math.sqrt(dx**2 + dy**2)

    if 2 > magnitude < 2:
        # If the positions are the same, return (0, 0)
        direction = (0, 0)
    else:
        direction = ((dx / magnitude), (dy / magnitude))
    
    return direction

def adjust_color(color, adjustment):
    # makes a color lighter or darker

    # check if color is pygame color
    if isinstance(color, pygame.Color):
        r = color.r
        g = color.g
        b = color.b
    else:
        r, g, b = color
    r = max(0, min(255, r + adjustment))
    g = max(0, min(255, g + adjustment))
    b = max(0, min(255, b + adjustment))
    return (r, g, b)