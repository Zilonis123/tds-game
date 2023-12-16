import json, pygame
from ..Entities.ttext import Ttext
from ..Visuals.renderers import text
from .wave import Wave


FRAMES_TEXT_ALIVE = 120

def is_wave_finished(render):
   return render.currentWave.isDone(render)

def wave_handler(render):
    if is_wave_finished(render):
        start_next_wave(render)
        

def wave_text(render):
    def tick(self,render):
        self.opacity -= 1
        if self.opacity == 0:
            render.ttext.remove(self)

    t = Ttext(f"Wave {render.wave}", render.screencenter, tick, "white", "center", "Nexa-Heavy.ttf", 50)
    render.ttext.append(t)

def start_next_wave(render):

    if render.waveStartedAt == -1:
        wave_text(render)
        render.waveStartedAt = render.ticks
        return

    if render.ticks-render.waveStartedAt != 255:
        return

    render.waveStartedAt = -1
    render.wave += 1

    
    wave = Wave(render.wave)

    render.currentWave = wave

    wave.spawn_all(render)


