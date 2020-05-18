import math
import pygame as py
import object
import config
import missile
import particle
import random

class Fighter(py.sprite.Sprite,object.Object):

    def __init__(self):
        py.sprite.Sprite.__init__(self)
        object.Object.__init__(self)
        self.imgs = [py.image.load("../images/fighter"+str(x)+".png") for x in range(1,6)]
        self.image = self.imgs[0]
        self.rect = self.image.get_rect()
        self.speed = 200
        self.turn_speed = config.fighter_turn_speed
        self.health = 100
        self.otherFighters = None
        self.frame = 1
        self.width = 80
        self.height = 80
        self.angle = 90
        self.pos = [100,100]
        self.health = 100
        self.killit = False
        self.rect.x = random.randint(1000, 2000)
        self.rect.y = random.randint(1000, 2000)
        self.launched_missiles = None
        self.launch_time = 0
        self.slowvalue = 1
        self.total_missiles = config.total_missiles

        self.particle_system = particle.ParticleSystem()

    def renderPosition(self, ref):
        super().renderPosition(ref)


    def rot_center(self):
        self.permimage = self.imgs[self.frame]
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



    def update(self,playerpos,speed,slowvalue):
        self.slowvalue = slowvalue
        self.frame = (self.frame+1)%5
        if not self.killit:
            if(len(self.launched_missiles.sprites())<config.launch_missiles_limit and self.total_missiles > 0and self.launch_time>config.launch_time):
                missile1 = missile.Missile()
                missile1.pos = list(self.pos)
                # missile1.v = self.v
                self.launched_missiles.add(missile1)
                self.launch_time = 0
                self.total_missiles-=1
            self.launch_time+=1*self.slowvalue

            ratio = (speed / config.normal_speed)
            if speed > config.normal_speed:
                self.speed = config.normal_speed

            elif 140 < speed < config.normal_speed:
                self.speed = speed
            else:
                self.speed = 140
            # if (config.missile_speed * ratio < 50):
            #     self.speed = 80
            # else:
            #     self.speed = config.missile_speed * ratio
            if len(self.otherFighters.sprites())>1:
                for fighter in self.otherFighters.sprites():
                    if fighter!= self:
                        dis = self.norm(self.sub_vec(self.pos,fighter.pos))
                        if(dis > 120):
                            rot_dir = self.sub_vec(playerpos, self.pos)
                            v_turn = self.unit(self.sub_vec(rot_dir, self.v))
                            v_turn = self.multiply(self.slowvalue, v_turn)
                            t1 = self.multiply(self.speed, self.v)
                            t2 = self.multiply(self.turn_speed, v_turn)
                            # print(t1,"----",t2)
                            self.v = self.add_vec(t1 ,t2 )
                        else:
                            self.v = fighter.v
            else:
                rot_dir = self.sub_vec(playerpos, self.pos)
                v_turn = self.unit(self.sub_vec(rot_dir, self.v))
                v_turn = self.multiply(self.slowvalue, v_turn)
                t1 = self.multiply(self.speed, self.v)
                t2 = self.multiply(self.turn_speed, v_turn)
                # print(t1,"----",t2)
                self.v = self.add_vec(t1, t2)
        else:
            self.kill()

            for i in self.particle_system.particles:
                if (i.size >= config.particle_expansion_size):
                    self.particle_system.particles.remove(i)
        # print("1  ",self.v)
        self.v = self.unit(self.v)
        # print("2  ",self.v)
        self.pos = self.add_vec(self.pos, self.multiply(self.speed * config.dt*slowvalue, self.v))
        if not self.killit:
            self.particle_system.add_particle(self.pos)
        self.rot_center()
        self.renderPosition(playerpos)
        self.rect.centerx = self.renderpos[0]
        self.rect.centery = self.renderpos[1]