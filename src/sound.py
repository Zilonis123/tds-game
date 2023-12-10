

def play(render, sound: str):
    sound = render.sounds.get(sound, False)
    if not sound:
        return

    sound.play()
