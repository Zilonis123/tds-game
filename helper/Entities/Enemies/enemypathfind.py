import math
import heapq
import pygame

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_path(screen, path, start, rect_size):
    current = start

    for dx, dy in path:
        new_x = current[0] + dx * rect_size
        new_y = current[1] + dy * rect_size
        pygame.draw.line(screen, "RED", current, (new_x, new_y), 5)
        current = (new_x, new_y)

def astar_pathfinding(map_rects, start, end):
    open_list = [start]
    came_from = {}
    cost_so_far = {start: 0}

    while open_list:
        current = open_list[0]

        if current == end:
            return reconstruct_path(came_from, end)

        open_list = open_list[1:]
        for dx, dy in [UP, DOWN, LEFT, RIGHT]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if not is_valid_move(map_rects, neighbor):
                continue
            
            new_cost = cost_so_far[current] + 1  # Assuming 1 is the cost to move from one cell to the adjacent cell
            
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                open_list.append(neighbor)
                came_from[neighbor] = current

    # If no path is found, return None
    return None

def is_valid_move(map_rects, neighbor):
    # Check if the move is valid by avoiding collisions with rectangles
    if neighbor[0] < 0 or neighbor[1] < 0:
        return False
    for rect in map_rects:
        if rect.collidepoint(neighbor):
            return False
    return True

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        previous = current
        current = came_from[current]
        dx = current[0] - previous[0]
        dy = current[1] - previous[1]
        path.append((dx, dy))
    path.reverse()
    return path