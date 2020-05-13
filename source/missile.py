import object
import numpy as np
import particle
import pygame as py
import config

class Missile(py.sprite.Sprite,object.Object):

    def __init__(self):
        object.Object.__init__(self)
        py.sprite.Sprite.__init__(self)
        self.speed = config.missile_speed
        self.turn_speed = config.missile_turn_speed
        self.particle_system = particle.ParticleSystem()
        self.permimage = py.image.load("../images/homissile.png")
        self.image = py.image.load("../images/homissile.png")
        self.rect =self.image.get_rect()
        self.rect.x = np.random.randint(1000,2000)
        self.rect.y = np.random.randint(1000,2000)
        self.fuel = config.missile_fuel
        self.killit = False

    def renderPosition(self,ref):
        super().renderPosition(ref)
        self.particle_system.renderPosition(ref)

    def rot_center(self):
        # self.permimage = py.transform.scale(self.permimage, (self.width, self.height))
        orig_rect = self.permimage.get_rect()
        rad = np.arccos(np.dot(self.unit(self.v),np.array([1,0])))
        rad2 = np.arccos(np.dot(self.unit(self.v), np.array([0, 1])))
        self.angle = np.rad2deg(rad)
        self.angle2 =  np.rad2deg(rad2)

        if self.angle2 >=90:
            rot_image = py.transform.rotate(self.permimage,-270 - (180-self.angle))
        else:
            rot_image = py.transform.rotate(self.permimage, -self.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = self.image.get_rect()
        # self.rect.centerx = 300
        # self.rect.centery = 300


    def update(self,playerpos,speed):

        if self.killit == False:
            rot_dir = playerpos - self.pos
            unit_dir = rot_dir/np.linalg.norm(rot_dir)
            ratio = (speed/config.normal_speed)
            if(config.missile_speed*ratio <50):
                self.speed = 80
            else:
                self.speed = config.missile_speed*ratio
            v_turn = self.unit(rot_dir - self.v)
            self.v = self.v*self.speed + v_turn*self.turn_speed
            self.fuel -= 0.5
        else:

            self.kill()

            for i in self.particle_system.particles:
                if(i.size >=config.particle_expansion_size):
                    self.particle_system.particles.remove(i)

        self.v = self.unit(self.v)
        self.pos += self.v*self.speed*config.dt
        if not self.killit:
            self.particle_system.add_particle(self.pos)
        self.rot_center()
        self.renderPosition(playerpos)
        self.rect.centerx = self.renderpos[0]
        self.rect.centery = self.renderpos[1]



