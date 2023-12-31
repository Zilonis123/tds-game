# this file will have a bunch of functions that will change how
# a turret or UIe looks

import pygame as pg
import math

def triangle_render(render, rect: pg.Rect, color: str | pg.Color, width=0, rotation_angle=0):
    x: int | float = rect.x
    y: int | float = rect.y
    w: int | float = rect.width
    h: int | float = rect.height

    rotation_angle: int = rotation_angle * -1

    # Calculate triangle vertices
    vertices: list[int | float] = [(x + w // 2, y), (x, y + h), (x + w, y + h)]

    if rotation_angle != 0:
        # Calculate rotation pivot point (center of the triangle)
        pivot = (x + w // 2, y + h // 2)

        # Rotate the vertices
        rotated_vertices = []
        for vertex in vertices:
            angle_rad = math.radians(rotation_angle)
            x_rotated = math.cos(angle_rad) * (vertex[0] - pivot[0]) - math.sin(angle_rad) * (vertex[1] - pivot[1]) + pivot[0]
            y_rotated = math.sin(angle_rad) * (vertex[0] - pivot[0]) + math.cos(angle_rad) * (vertex[1] - pivot[1]) + pivot[1]
            rotated_vertices.append((x_rotated, y_rotated))
    else:
        rotated_vertices: list[int | float] = vertices
        
    pg.draw.polygon(render.screen, color, rotated_vertices, width)


def square_render(render, rect: pg.Rect, color: str | pg.Color, width=0, rotation_angle=0, border=0):
    if isinstance(color, pg.Color):
        # draw with alpha / transparency
        shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
        pg.draw.rect(shape_surf, color, shape_surf.get_rect(), border_radius=border)
        render.screen.blit(shape_surf, rect)
        return


    if rotation_angle != 0:
        # Create a square with a specified rotation angle
        rotated_surface = pg.Surface(rect.size, pg.SRCALPHA)
        rotated_surface.fill((0, 0, 0, 0))  # Fill with transparent color
        square = pg.draw.rect(rotated_surface, color, (0, 0, rect.width, rect.height), width, border_radius=border)

        # Rotate the square
        rotated_square = pg.transform.rotate(rotated_surface, rotation_angle)

        # Get the rect of the rotated square
        rotated_rect = rotated_square.get_rect(center=rect.center)

        # Blit the rotated square onto the screen
        render.screen.blit(rotated_square, rotated_rect.topleft)
    else:
        pg.draw.rect(render.screen, color, rect, width, border_radius=border)


def hexagon_render(render, rect: pg.Rect, color: str | pg.Color, width=0, rotation_angle=0):
    x, y=rect.center
    size = rect.width / math.sqrt(3)

    # future me. I am very sorry for this code you dont understand
    angle_deg = 360 / 6
    vertices = []
    for i in range(6):
        angle_rad = math.radians(angle_deg * i + rotation_angle)
        hexagon_x = x + size * math.cos(angle_rad)
        hexagon_y = y + size * math.sin(angle_rad)
        vertices.append((hexagon_x, hexagon_y))

    pg.draw.polygon(render.screen, color, vertices, width)

def circle_renderer(render, rect: pg.Rect, color: str | pg.Color, width=0, radius=15):
    pg.draw.circle(render.screen, color, rect.center, radius, width)

def draw_circle_alpha(render, color: str | pg.Color, center: tuple[int | float, int | float], radius: int | float):
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    render.screen.blit(shape_surf, target_rect)

def healthbar(render, pos: tuple[int | float, int | float], health: int, maxhealth: int, size=5):
    TRANSPARENCY = 220

    darkred = pg.Color(83,0,0, TRANSPARENCY)
    green = pg.Color(0,206,17, TRANSPARENCY)
    
    x,y=pos

    uSize = 25 # uSize - universal size // half of the line

    surface = pg.Surface(render.screen.get_size(), pg.SRCALPHA)

    length: int = round((health/maxhealth)*(uSize*2))
    
    # empty health
    pg.draw.line(surface, darkred, (x-uSize+length, y), (x+uSize, y), size)

    # full health
    pg.draw.line(surface, green, (x-uSize, y), ((x-uSize)+length,y), size)

    render.screen.blit(surface, (0,0))

def text(render, text: str, color: pg.Color | str, pos: tuple[int | float, int | float], size=18, type="center", 
font="freesansbold.ttf", background=False, backgroundClr=pg.Color(0,0,0,70), opacity=255) -> pg.Rect:
    # init font
    type = type.lower()

    # get a rendered font
    f = render.fonts.get(font+f"-{size}", False)
    if not f:
        f = pg.font.Font(font, size)
        render.fonts[f"{font}-{size}"] = f

    surface = f.render(text, True, color)
    if opacity != 255:
        surface.set_alpha(opacity)

    rect = surface.get_rect()

    if type == "center":
        rect.center = pos
    elif type == "topleft":
        rect.topleft = pos
    elif type == "topright":
        rect.topright = pos
    elif type == "bottomleft":
        rect.bottomleft = pos
    elif type == "bottomright":
        rect.bottomright = pos

    if background:
        square_render(render, rect, backgroundClr)

    render.screen.blit(surface, rect)

    return rect

def image(render, image_name: str, pos: tuple[int, int]):

    if isinstance(image_name, str):
        img_surface = render.imgs.get(image_name, None)
    else:
        img_surface = image_name


    if img_surface == None:
        return
    
    render.screen.blit(img_surface, pos)