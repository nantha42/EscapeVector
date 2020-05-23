import pygame as py
from pygame.locals import *


class BigFontSystem:
    def __init__(self):
        # self.basicfont = py.font.SysFont(None,20)

        self.basicfont = py.font.Font("../font/karma future.ttf",30)

    def draw(self,text,color = (255,255,255)):
        text = self.basicfont.render(text, True, color)
        textrect = text.get_rect()
        return [text,textrect]

class SmallFontSystem:
    def __init__(self):

        self.basicfont = py.font.Font("../font/karma future.ttf",20)

    def draw(self,text,color = (255,255,255)):
        text = self.basicfont.render(text, True, color)
        textrect = text.get_rect()
        return [text,textrect]

