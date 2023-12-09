# this file will contain anything to make the code more readable
import math
import pygame as pg

def translate_rect_to_circ(rect: pg.Rect) -> tuple[float, float]:
    # converts rects pos to match a circles pos -- moves rect to its center
    return (rect.x-rect.width//2, rect.y-rect.height//2)

def changeTuple(tuple: tuple[float, float], changeBy: tuple[float, float]) -> tuple[float, float]:
    return (tuple[0]+changeBy[0], tuple[1]+changeBy[1])

def remove_string(base_string, prefix):
    if base_string.startswith(prefix):
        return base_string[len(prefix):]
    else:
        return base_string


def diagonally_pathfind(b: tuple[float, float], a: tuple[float, float]) -> tuple[float | float]:
    dx: int = round(a[0] - b[0])
    dy: int = round(a[1] - b[1])

    magnitude: int|float = math.sqrt(dx**2 + dy**2)

    if 2 > magnitude < 2:
        direction = (0, 0)
    else:
        direction = ((dx / magnitude), (dy / magnitude))

    return direction

def adjust_color(color: str | pg.Color, adjustment: int) -> pg.Color:
    # makes a color lighter or darker

    # check if color is pygame color
    if not isinstance(color, pg.Color):
        color = pg.Color(color)

    r: int = color.r
    g: int = color.g
    b: int = color.b
    r: int = max(0, min(255, r + adjustment))
    g: int = max(0, min(255, g + adjustment))
    b: int = max(0, min(255, b + adjustment))
    return pg.Color(r, g, b)

def pointInCircle(p1: tuple[int|float, int|float], circleCenter: tuple[int|float, int|float], radius: int) -> bool:
    d: float = math.sqrt((p1[0] - circleCenter[0])**2+(p1[1] - circleCenter[1]) ** 2)
    return d <= radius



def findenemy_by_id(render, uid: str):
    enemy = [enemy for enemy in render.enemies if enemy.uid == uid]
    if len(enemy) == 0:
        return None
        
    return enemy[0]




def findturret_by_id(render, uid: str):
    turret: Turret = [turret for turret in render.turrets if turret.uid == uid]
    if len(turret) == 0:
        return None

    return turret[0]