import math

# self is enemy

def find_turret(self, render, ignore=[]):
    closest_turret = None
    min_distance = float('inf')

    point = self.rect.center

    for turret in render.turrets:
        rect = turret.rect
        # Calculate the center of the rectangle
        rect_center = (rect.left + rect.width / 2, rect.top + rect.height / 2)

        # Calculate the distance between the point and the rectangle's center
        distance = math.hypot(point[0] - rect_center[0], point[1] - rect_center[1])

        if distance < min_distance:
            min_distance = distance
            closest_turret = turret

    return closest_turret