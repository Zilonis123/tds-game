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

def square_render(render, rect, color, width=0, rotation_angle=0):
    # Create a square with a specified rotation angle
    rotated_surface = pg.Surface(rect.size, pg.SRCALPHA)
    rotated_surface.fill((0, 0, 0, 0))  # Fill with transparent color
    square = pg.draw.rect(rotated_surface, color, (0, 0, rect.width, rect.height), width)

    # Rotate the square
    rotated_square = pg.transform.rotate(rotated_surface, rotation_angle)

    # Get the rect of the rotated square
    rotated_rect = rotated_square.get_rect(center=rect.center)

    # Blit the rotated square onto the screen
    render.screen.blit(rotated_square, rotated_rect.topleft)


def hexagon_render(render, rect, color, isOutline=0, rotation_angle=0):
    x,y=rect.center
    size = rect.width / math.sqrt(3)

    # future me. I am very sorry for this code you dont understand
    angle_deg = 360 / 6
    vertices = []
    for i in range(6):
        angle_rad = math.radians(angle_deg * i + rotation_angle)
        hexagon_x = x + size * math.cos(angle_rad)
        hexagon_y = y + size * math.sin(angle_rad)
        vertices.append((hexagon_x, hexagon_y))

    pg.draw.polygon(render.screen, color, vertices, isOutline)

def circle_renderer(render, rect, color, isOutline=0, radius=15):
    pg.draw.circle(render.screen, color, rect.center, radius, isOutline)

def draw_circle_alpha(render, color, center, radius):
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    render.screen.blit(shape_surf, target_rect)

def healthbar(render, pos, health, maxhealth, size=5):
    darkred = pg.Color(83,0,0)
    green = pg.Color(0,206,17)
    
    x,y=pos

    uSize = 25 # uSize - universal size // half of the line

    # line background
    pg.draw.line(render.screen, darkred, (x-uSize, y), (x+uSize, y), size)

    length = round((health/maxhealth)*(uSize*2))
    pg.draw.line(render.screen, green, (x-uSize, y), ((x-uSize)+length,y), size)
    text(render, str(health), "white", (x, y-5), 10)

def text(render, text, color, pos, size=18):
    # init font

    font = pg.font.Font('freesansbold.ttf', size)
    surface = font.render(text, True, color)

    rect = surface.get_rect()
    rect.center = pos

    render.screen.blit(surface, rect)