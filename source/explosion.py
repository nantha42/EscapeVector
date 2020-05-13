import pygame as py
import numpy as np

class Explosion:
    def __init__(self):
        self.size = 4
        self.images = []
        for i in range(1,12):
            img = py.image.load("../images/exp"+str(i)+".png").convert_alpha()
            img = py.transform.scale(img,(128*self.size,128*self.size))
            self.images.append(img)

    def get_image(self,i):
        return self.images[i]
