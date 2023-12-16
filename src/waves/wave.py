import json, random, pygame
from ..Entities.enemies import Enemy

class Wave():
    def __init__(self, wave: int):
        f = open("info/waves.json")
        data = json.load(f)
        data = self._getWaveInfo(data, wave)

        self.enemies = data


    def spawn_all(self, render) -> None:
        for enemy, amount in self.enemies.items():
            for i in range(amount):
                pos = self.generate_random_coordinates(render)
                e = Enemy(enemy, pos)
                render.enemies.append(e)

    def _getWaveInfo(self, data, wave: int) -> dict:
        waveInfo = data.get(str(wave), None)
        if waveInfo == None:
            return self._getWaveInfo(data, wave-1) if wave > 0 else {}
        return waveInfo


    def generate_random_coordinates(self, render):
        box_x = 0
        box_y = 0
        box_width = render.WIDTH+100
        box_height = render.HEIGHT+100
        rect = pygame.Rect(-50,-50,box_width, box_height)
        while True:
            x = random.uniform(-100, render.WIDTH+100)
            y = random.uniform(-100, render.HEIGHT+100)

            # Check if the coordinates are outside the box
            if not rect.collidepoint(x,y):
                return x, y

    def isDone(self, render) -> bool:
        return len(render.enemies) == 0