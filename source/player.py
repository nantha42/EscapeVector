
from object import Object
import particle
import config
import pygame as py
import spritesheet
import math

class Player(py.sprite.Sprite,Object):
    def __init__(self):
        Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.speed= config.normal_speed
        self.turn_speed = 2
        self.particle_system = particle.ParticleSystem()
        self.imgs = []
        self.health = 100
        self.live = True
        for i in range(6):
            self.imgs.append(py.image.load("../images/top"+str(i+1)+".png"))

        self.frame = 0
        self.width = 80
        self.height = 80

        self.permimage = self.imgs[self.frame]
        self.permimage = py.transform.scale(self.permimage,(self.width,self.height))
        self.image = py.image.load("../images/ship.png")
        self.rect = self.permimage.get_rect()
        self.angle = 0

    def rot_center(self):
        self.permimage = self.imgs[int(self.frame/3)]
        self.permimage = py.transform.scale(self.permimage, (self.width,self.height))
        orig_rect = self.permimage.get_rect()
        # rad = np.arccos(np.dot(self.unit(self.v),np.array([1,0])))
        # self.angle = np.rad2deg(rad)
        rot_image = py.transform.rotate(self.permimage, -self.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = self.image.get_rect()
        self.rect.centerx = config.screen_width/2
        self.rect.centery = config.screen_height/2


    def turn_left(self):
        self.angle -= self.turn_speed

    def turn_right(self):
        self.angle += self.turn_speed

    def throttleUp(self):
        if self.speed < config.normal_speed:
            self.speed+=3

    def throttleDown(self):
        if self.speed > config.normal_speed/3:
            self.speed-= 3


    def update(self):

        # dir = np.array(mousepos) - np.array((300,300))
        # dir = self.unit(dir)

        r = math.radians(self.angle)
        dir = [math.cos(r),math.sin(r)]

        self.v = self.add_vec(self.multiply(self.speed, self.v), self.multiply(self.turn_speed * 100, dir))
        self.v = self.unit(self.v)
        self.pos = self.add_vec(self.pos,self.multiply(self.speed*config.dt,self.v))

        r = math.radians(-self.angle-180+90)
        r1 = math.radians(-self.angle - 180 - 90)

        p1 = self.multiply(5,[math.cos(r),math.sin(r)])
        p2 = self.multiply(5,[math.cos(r1), math.sin(r1)])
        self.particle_system.add_particle(self.add_vec(self.pos, p1))
        self.particle_system.add_particle(self.add_vec(self.pos, p2))
        self.rot_center()
        self.frame = (self.frame+1)%18

    def renderPosition(self,ref):
        self.particle_system.renderPosition(self.pos)