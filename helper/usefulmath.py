# this file will contain anything to make the code more readable

def translate_rect_to_circ(rect):
    # converts rects pos to match a circles pos -- moves rect to its center
    return (rect.x-rect.width//2, rect.y-rect.height//2)