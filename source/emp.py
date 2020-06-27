import pygame as py
import object
import config
import math

class Emp(object.Object,py.sprite.Sprite):

    def __init__(self,direction,pos):
        object.Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.life = 100
        self.pos = list(pos)
        self.direction = list(self.unit(direction))
        self.speed = config.emp_speed
        self.angle = -self.calculate_angle(self.direction)
        self.v = self.multiply(self.speed, self.direction)
        self.image_width = 180
        self.image_height = 180
        # r = [self.pos[0]-100,self.pos[1]-100]

        self.image = py.Surface.convert_alpha(py.Surface((self.image_width,self.image_height)))
        self.image.fill((0,0,0,0))
        py.draw.arc(self.image, (50, 50, 205), [0, 0, 180, 180], math.radians(self.angle - 60),
                    math.radians(self.angle + 60), 8)
        self.rect = self.image.get_rect()

    def update(self,playerpos,slowvalue):
        if self.life <=0:
            # print("killed")
            self.kill()
        else:
            self.life -= slowvalue*1
        # print(self.life)
            # print(self.life)
        self.v = self.multiply(self.speed, self.direction)
        self.pos = self.add_vec(self.pos, self.multiply(config.dt * slowvalue, self.v))
        self.renderPosition(playerpos)
        self.rect.x = self.renderpos[0]-45
        self.rect.y = self.renderpos[1]-45