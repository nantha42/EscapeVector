import pygame as py
import fighter
import missile
import vectors
import math

class Minimap:

    def __init__(self):
        self.permimage = py.image.load("../images/mapoutline.png")
        self.permimage = py.transform.scale(self.permimage,(128,128))
        self.image = self.permimage.copy()
        self.positions = []
        pass

    def update(self,sprites,player):
        self.positions = []
        for sprite in sprites:
            k = vectors.sub_vec(sprite.pos,player.pos)
            k = [k[0]/30,k[1]/30]
            d = vectors.norm(k)

            if(d<50):

                k = [k[0]+63,k[1]+63]
                self.positions.append(k)
        self.draw()

    def draw(self):
        self.image = self.permimage.copy()
        for pos in self.positions:
            py.draw.circle(self.image,(255,0,0),pos,2,2)

