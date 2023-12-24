

def play(render, sound: str) -> bool:
    sound = render.sounds.get(sound, False)
    if not sound:
        return False

    sound.play()
    return sound

def play_music(render, sound: str):
    if render.musicPlaying != None:
        render.musicPlaying.fadeout(500)
    
    s = play(render, sound)
    if s:
        render.musicPlaying = s