import object

import particle
import pygame as py
import config
import math
import random
import time

class Missile(py.sprite.Sprite, object.Object):

    def __init__(self):
        object.Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.speed = config.missile_speed
        self.turn_speed = config.missile_turn_speed
        self.particle_system = particle.ParticleSystem()
        self.permimage = py.image.load("../images/homissile.png")
        self.image = py.image.load("../images/homissile.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1000, 2000)
        self.rect.y = random.randint(1000, 2000)
        self.fuel = random.randint(config.missile_fuel-50,config.missile_fuel)
        self.killit = False
        self.created_time = time.time()
        self.activated = False
        self.slowvalue = 1


    def renderPosition(self, ref):
        super().renderPosition(ref)
        self.particle_system.renderPosition(ref)

    def rot_center(self):
        # self.permimage = py.transform.scale(self.permimage, (self.width, self.height))
        orig_rect = self.permimage.get_rect()
        rad = math.acos(self.dot(self.unit(self.v), [1, 0]))
        rad2 = math.acos(self.dot(self.unit(self.v), [0, 1]))
        self.angle = math.degrees(rad)
        self.angle2 = math.degrees(rad2)

        if self.angle2 >= 90:
            rot_image = py.transform.rotate(self.permimage, -270 - (180 - self.angle))
        else:
            rot_image = py.transform.rotate(self.permimage, -self.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = self.image.get_rect()
        # self.rect.centerx = 300
        # self.rect.centery = 300

    def update(self, playerpos, speed,slowvalue):
        self.slowvalue = slowvalue
        if self.killit == False:
            rot_dir = self.sub_vec(playerpos,self.pos)
            v_turn = self.unit(self.sub_vec(rot_dir ,self.v))
            v_turn = self.multiply(self.slowvalue,v_turn)
            self.v = self.add_vec(self.multiply(self.speed,self.v), self.multiply(self.turn_speed,v_turn))
            self.fuel -= 0.5*self.slowvalue

        else:
            self.kill()
            for i in self.particle_system.particles:
                if (i.size >= config.particle_expansion_size):
                    self.particle_system.particles.remove(i)

        self.v = self.unit(self.v)
        self.pos = self.add_vec(self.pos,self.multiply(self.speed*config.dt*self.slowvalue,self.v))
        if not self.killit:
            self.particle_system.add_particle(self.pos)
        self.rot_center()
        self.renderPosition(playerpos)
        self.rect.centerx = self.renderpos[0]
        self.rect.centery = self.renderpos[1]

        if time.time() -self.created_time > 0.5:
            self.activated = True

        # self.rect.x = self.renderpos[0]
        # self.rect.y = self.renderpos[1]