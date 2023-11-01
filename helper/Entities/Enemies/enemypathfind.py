import math
import heapq
import pygame

from ...usefulmath import diagonally_pathfind


def draw_path(screen, path, start, rect_size):
    current = start
    a = 0

    for dx, dy in path:
        new_x = current[0] + dx
        new_y = current[1] + dy
        if a%4 == 0: pygame.draw.circle(screen, "red", current, 3)
        current = (new_x, new_y)
        a+=1

def astar_pathfinding(map_rects, start: tuple, end: tuple, speed: int):
    path: list[tuple] = []
    x,y = start
    at = (round(x), round(y))
    x,y = end
    end = (round(x), round(y))




    done = False
    while not done:

        dx,dy = diagonally_pathfind(at, end)
        dx = round(dx*speed)
        dy = round(dy*speed)
        at = (at[0]+dx, at[1]+dy)
        path.append((dx, dy))

        if at[0] == end[0]: print("a")

    
        if len(path) > 700 or at[0] == end[0]:
            done = True
    
    return path