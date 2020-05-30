from object import Object
import particle
import config
import pygame as py
import spritesheet
import math
import random
import time

class Player(py.sprite.Sprite,Object):
    def __init__(self):
        Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.speed= config.normal_speed
        self.turn_speed = 3
        self.particle_system = particle.ParticleSystem()
        self.vParticle_system = particle.VelocityParticleSystem()
        self.imgs = []
        self.sonic_imgs = []
        self.boom_imgs = []
        self.health = config.player_health
        self.live = True
        self.turbo = 100
        self.emp_affected = False
        self.releasing_turbo = False
        self.slowvalue = 1
        self.emp_duration = 0

        for i in range(6):
            self.imgs.append(py.image.load("../images/top"+str(i+1)+".png"))
        for i in range(6):
            self.sonic_imgs.append(py.image.load("../images/sonic/sonic"+str(i+1)+".png"))
        for i in range(8):
            self.boom_imgs.append(py.image.load("../images/sonic/boom/boom"+str(i+1)+".png"))

        self.damaging = False
        self.damageshowindex = 0

        self.frame = 0
        self.sonic_frame = 0
        self.width = 80
        self.height = 80
        self.damage_image = py.image.load("../images/damage.png")
        self.permimage = self.imgs[self.frame]
        self.permimage = py.transform.scale(self.permimage,(self.width,self.height))
        self.image = py.image.load("../images/ship.png")
        self.rect = self.permimage.get_rect()
        self.angle = 0
        self.shoottimer = time.time()

    def rot_center(self):
        if self.speed > 300 and self.speed < 324:
            ind = int((self.speed - 300) / 3)

            self.permimage = self.boom_imgs[ind]
            self.permimage = py.transform.scale(self.permimage,(self.width*2,self.height*2))
        else:
            if not self.releasing_turbo:
                if self.damaging:
                    self.permimage = self.damage_image.copy()
                    self.damageshowindex+=1
                    if self.damageshowindex > 4:
                        self.damaging = False
                        self.damageshowindex = 0
                else:
                    self.permimage = self.imgs[int(self.frame/3)]
            else:

                self.permimage = self.sonic_imgs[int(self.frame/3)]

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


    def release_turbo(self):

        if self.turbo>0.5:
            self.releasing_turbo = True
            self.turbo-=0.5*self.slowvalue
            if self.speed < config.normal_speed+200:
                self.speed += 5*self.slowvalue

        if self.turbo == 0.0:
            self.releasing_turbo = False

    def stop_turb(self):
        self.releasing_turbo = False

    def turn_left(self):
        self.angle -= self.turn_speed*self.slowvalue

    def turn_right(self):
        self.angle += self.turn_speed*self.slowvalue

    def throttleUp(self):
        # print(self.turbo)
        if self.turbo < 100 and not self.releasing_turbo:
            self.turbo += 1*self.slowvalue

        if self.speed < config.normal_speed and not self.releasing_turbo:
            self.speed+=3*self.slowvalue

        elif self.speed > config.normal_speed:
            self.speed -= 3*self.slowvalue

    def throttleDown(self):
        if self.speed > config.normal_speed/3 and self.releasing_turbo == False:
            self.speed-= 3*self.slowvalue


    def update(self,slowvalue):

        if self.emp_affected == True:
            self.emp_duration = 1000
            self.emp_affected = False

        self.slowvalue = slowvalue
        r = math.radians(self.angle)
        dir = [math.cos(r),math.sin(r)]
        if self.emp_duration>0:
            self.emp_duration -= 3*slowvalue
            print(self.emp_duration)

        if self.emp_duration >0:
            if self.speed > 160:
                self.speed-= 1
            else:
                self.speed = 160

        self.v = self.add_vec(self.multiply(self.speed, self.v), self.multiply(self.turn_speed * 100, dir))
        self.v = self.unit(self.v)
        self.pos = self.add_vec(self.pos,self.multiply(self.speed*config.dt*slowvalue,self.v))

        r = math.radians(-self.angle-180+90)
        r1 = math.radians(-self.angle - 180 - 90)
        r2 = math.radians(self.angle+random.randint(-90,90))
        p1 = self.multiply(5,[math.cos(r),math.sin(r)])
        p2 = self.multiply(random.randint(10, 45), [math.cos(r), math.sin(r)])
        if self.live:
            self.particle_system.add_particle(self.add_vec(self.pos, p1))
            vv = [self.v[0], self.v[1]]
            self.vParticle_system.add_particle(self.add_vec(self.pos, p2), vv)

        self.rot_center()
        self.frame = (self.frame+1)%18
        #sounds

    def renderPosition(self):
        self.particle_system.renderPosition(self.pos)
        self.vParticle_system.renderPosition(self.pos,self.slowvalue)