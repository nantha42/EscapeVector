import pygame as py
import object
import config
import math

class Emp(object.Object,py.sprite.Sprite):

    def __init__(self,direction):
        object.Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.life = 1000
        self.image = py.Surface.convert_alpha(py.Surface((90,90)))
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()
        self.direction = list(self.unit(direction))
        self.speed = config.emp_speed
        self.angle = self.calculate_angle(self.direction)-90
        self.v = self.multiply(self.speed, self.direction)
        r = [self.pos[0]-100,self.pos[1]-100]
        py.draw.arc(self.image,(45,30,255),[r[0],r[1],200,200],math.radians(self.angle-60),math.radians(self.angle+60),8)
        py.draw.circle(self.image,(200,200,200,255),r,10,3)

    def update(self,playerpos,slowvalue):
        if self.life <0:
            self.kill()
        else:
            self.life -= slowvalue*1
        self.pos = self.add_vec(self.pos, self.multiply(self.speed * config.dt * slowvalue, self.v))
        self.renderPosition(playerpos)
        self.rect.x = self.renderpos[0]
        self.rect.y = self.renderpos[1]
