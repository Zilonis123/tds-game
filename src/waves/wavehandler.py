import json, random, pygame
from .Entities.enemies import Enemy
from .Visuals.renderers import text


FRAMES_TEXT_ALIVE = 120

def is_wave_finished(render):
   return render.waveIsLoading == False and len(render.enemies) == 0 

def wave_handler(render):
    if is_wave_finished(render):
        start_next_wave(render)
        

def wave_text(render):
    
    text(render, f"Wave {render.wave}", "white", render.screencenter, size=50, 
    font="Nexa-Heavy.ttf", opacity=255-round((render.ticks-render.waveStartedAt)/FRAMES_TEXT_ALIVE*255))


def start_next_wave(render):

    if render.waveStartedAt == -1:
        render.waveStartedAt = render.ticks

    if render.ticks-render.waveStartedAt <= FRAMES_TEXT_ALIVE:
        wave_text(render)
        return

    render.waveStartedAt = -1
    render.wave += 1

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
    box_width = render.WIDTH+100
    box_height = render.HEIGHT+100
    rect = pygame.Rect(-50,-50,box_width, box_height)
    while True:
        x = random.uniform(-100, render.WIDTH+100)
        y = random.uniform(-100, render.HEIGHT+100)

        # Check if the coordinates are outside the box
        if not rect.collidepoint(x,y):
            return x, y

def getNextWave(render, data, wave: int) -> dict:
    waveInfo = data.get(str(wave), None)
    if waveInfo == None:
        return getNextWave(render, data, wave-1)
    return waveInfo