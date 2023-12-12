import json, random
from .Entities.enemies import Enemy


def is_wave_finished(render):
   return render.waveIsLoading == False and len(render.enemies) == 0 

def start_next_wave(render):
    f = open("info/waves.json")
    data = json.load(f)
    
    waveInfo = getNextWave(render, data, render.wave)
    
    for enemy, amount in waveInfo.items():
        for i in range(amount):
            pos = generate_random_coordinates(render)
            e = Enemy(enemy, pos)
            render.enemies.append(e)


def generate_random_coordinates(render):
    box_x = 0
    box_y = 0
    box_width = render.WIDTH
    box_height = render.HEIGHT
    while True:
        x = random.uniform(-10, render.WIDTH+10)
        y = random.uniform(-10, render.HEIGHT+10)

        # Check if the coordinates are outside the box
        if not (box_x < x < box_x + box_width and box_y < y < box_y + box_height):
            return x, y

def getNextWave(render, data, wave: int) -> dict:
    waveInfo = data.get(str(wave), None)
    if waveInfo == None:
        return getNextWave(render, data, wave-1)
    return waveInfo