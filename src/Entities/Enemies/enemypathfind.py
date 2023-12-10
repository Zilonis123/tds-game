import math
import heapq
import pygame

from ...usefulmath import diagonally_pathfind
from ...decorators import timer


def draw_path(screen, path: list[tuple[int,int]], start: tuple[float, float], rect_size: int):
    current = start
    a = 0

    clr = "RED"

    for dx, dy in path:
        new_x = current[0] + dx
        new_y = current[1] + dy
        if a%4 == 0: pygame.draw.circle(screen, clr, current, 3)
        current = (new_x, new_y)
        a+=1


MAX_PATH_LENGTH = 500
def astar_pathfinding(start: tuple[int, int], end: tuple[int, int], speed: int):
    path: list[tuple] = []
    x, y = start
    at = (round(x), round(y))
    x, y = end
    end = (round(x), round(y))

    while 1==1:
        dx, dy = diagonally_pathfind(at, end)
        scaled_dx, scaled_dy = round(dx * speed), round(dy * speed)
        at = (at[0] + scaled_dx, at[1] + scaled_dy)
        path.append((scaled_dx, scaled_dy))

        if len(path) > MAX_PATH_LENGTH or (dx, dy) == (0, 0):
            break

    return path

def point_collides_with_rect(point, rect):
    # Calculate the distances from the point to each side of the rectangle
    left_dist = point[0] - rect.left
    right_dist = rect.right - point[0]
    top_dist = point[1] - rect.top
    bottom_dist = rect.bottom - point[1]

    # Determine which side the point is colliding with
    min_dist = min(left_dist, right_dist, top_dist, bottom_dist)
    if min_dist == left_dist:
        return "left"
    elif min_dist == right_dist:
        return "right"
    elif min_dist == top_dist:
        return "top"
    else:
        return "bottom"