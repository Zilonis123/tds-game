from ..Visuals.renderers import text
class Ttext():

    def __init__(self, text: str, pos: tuple[int,int], func, color="black"):
        self.text = text
        self.pos = pos
        self.func = func
        self.color = color
        self.timeAlive = 0
    
    def draw(self, render):
        text(render, self.text, self.color, self.pos, type="topright")