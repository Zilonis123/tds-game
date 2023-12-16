from ..Visuals.renderers import text
from dataclasses import dataclass, field

class Ttext():
    def __init__(self, text: str, pos: tuple[int,int], func, color: str, alignment="topright", 
    font="Nexa-Heavy.ttf", font_size=18):
        self.text = text
        self.pos = pos
        self.func = func
        self.color = color
        self.alignment = alignment
        self.font = font
        self.font_size = font_size
        
        self.timeAlive = 0
        self.opacity = 255
    
    def draw(self, render):
        text(render, self.text, self.color, self.pos, type=self.alignment, opacity=self.opacity, font=self.font,
        size=self.font_size)