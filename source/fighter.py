import math
import pygame as py
import object
import config
import missile
import particle
import random
import time


class Fighter(py.sprite.Sprite, object.Object):

    def __init__(self):
        py.sprite.Sprite.__init__(self)
        object.Object.__init__(self)
        self.imgs = [py.image.load("../images/fighter" + str(x) + ".png") for x in range(1, 6)]
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
        self.noactiontime = 0
        self.shoot = False
        self.pos = [100, 100]
        self.health = 100
        self.killit = False
        self.rect.x = random.randint(1000, 2000)
        self.rect.y = random.randint(1000, 2000)
        self.launched_missiles = None
        self.launch_time = 0
        self.turnv = None
        self.slowvalue = 1
        self.total_missiles = config.total_missiles
        self.shoottimer = time.time()
        self.angle = 0
        self.particle_system = particle.ParticleSystem()

        # Ai variables
        self.turnaway = False
        self.slowdown = False

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

    def receive_signal(self, signal):
        if signal[0] == "turnaway":
            self.turnaway = True
            self.turnv = list(signal[1])

        if signal[0] == "noturnaway":
            self.turnaway = False
            self.turnv = False

        if signal[0] == "slowdown":
            self.slowdown = True

        if signal[0] == "noslowdown":
            self.slowdown = False

    def update(self, playerpos, speed, slowvalue, player_live):
        if self.health <= 0:
            self.killit = True
        missile_attack = False
        shooting = False
        direc = self.sub_vec(playerpos, self.pos)
        dis = self.norm(direc)

        if dis > 1500 or self.noactiontime > 70:
            missile_attack = True
        else:
            shooting = True

        self.slowvalue = slowvalue
        self.frame = (self.frame + 1) % len(self.imgs)

        if not player_live:
            self.shoot = False
        if not self.killit:
            if player_live:

                if missile_attack:
                    self.noactiontime = 0
                    if (len(
                            self.launched_missiles.sprites()) < config.launch_missiles_limit and self.total_missiles > 0 and self.launch_time > config.launch_time):
                        missile1 = missile.Missile()
                        missile1.pos = list(self.pos)
                        # missile1.v = self.v
                        self.launched_missiles.add(missile1)
                        self.launch_time = 0
                        self.total_missiles -= 1

                    self.launch_time += 1 * self.slowvalue
                elif shooting:
                    ang = math.degrees(self.angle_2vec(self.v, direc))
                    # print(ang)
                    self.noactiontime = 0
                    if ang < 10:
                        self.shoot = True
                    else:
                        self.shoot = False
                    # print(math.degrees(ang))
                else:
                    self.noactiontime += 1

                if self.slowdown:
                    self.speed = 200
                else:
                    self.speed = config.fighter_speed

                rot_dir = self.sub_vec(playerpos, self.pos)
                v_turn = self.unit(self.sub_vec(rot_dir, self.v))
                v_turn = self.multiply(self.slowvalue, v_turn)
                t1 = self.multiply(self.speed, self.v)
                t2 = self.multiply(self.turn_speed, v_turn)
                # print(t1,"----",t2)
                if not self.slowdown:
                    self.v = self.add_vec(t1, t2)
        else:
            self.kill()
            for i in self.particle_system.particles:
                if (i.size >= config.particle_expansion_size):
                    self.particle_system.particles.remove(i)


        self.v = self.unit(self.v)
        self.pos = self.add_vec(self.pos, self.multiply(self.speed * config.dt * slowvalue, self.v))
        if not self.killit:
            self.particle_system.add_particle(self.pos)
        self.rot_center()
        self.renderPosition(playerpos)
        self.rect.centerx = self.renderpos[0]
        self.rect.centery = self.renderpos[1]
        self.angle = self.calculate_angle(self.v)

class EmpFighter(Fighter):
    def __init__(self):
        Fighter.__init__(self)
        self.imgs = [py.image.load("../images/empjet" + str(x) + ".png") for x in range(1, 5)]
        self.active_emp = None

    def update(self, playerpos, speed, slowvalue, player_live):
        if self.health <= 0:
            self.killit = True
        missile_attack = False
        shoot_emp = False
        direc = self.sub_vec(playerpos, self.pos)
        dis = self.norm(direc)

        if dis > 1500 or self.noactiontime > 70:
            pass
        else:
            shoot_emp = True

        self.slowvalue = slowvalue
        self.frame = (self.frame + 1) % len(self.imgs)

        if not player_live:
            self.shoot = False
        if not self.killit:
            if player_live:
                # if missile_attack:
                #     self.noactiontime = 0
                    # if (len(
                    #         self.launched_missiles.sprites()) < config.launch_missiles_limit and self.total_missiles > 0 and self.launch_time > config.launch_time):
                    #     # missile1 = missile.Missile()
                        # missile1.pos = list(self.pos)
                        # self.launched_missiles.add(missile1)
                        # self.launch_time = 0
                        # self.total_missiles -= 1
                    # self.launch_time += 1 * self.slowvalue
                if shoot_emp:
                    ang = math.degrees(self.angle_2vec(self.v, direc))
                    self.noactiontime = 0
                    if ang < 10:
                        self.shoot = True
                    else:
                        self.shoot = False
                else:
                    self.noactiontime += 1
                if self.slowdown:
                    self.speed = 200
                else:
                    self.speed = config.fighter_speed
                rot_dir = self.sub_vec(playerpos, self.pos)
                v_turn = self.unit(self.sub_vec(rot_dir, self.v))
                v_turn = self.multiply(self.slowvalue, v_turn)
                t1 = self.multiply(self.speed, self.v)
                t2 = self.multiply(self.turn_speed, v_turn)

                if not self.slowdown:
                    self.v = self.add_vec(t1, t2)
        else:
            self.kill()
            for i in self.particle_system.particles:
                if (i.size >= config.particle_expansion_size):
                    self.particle_system.particles.remove(i)

        self.v = self.unit(self.v)
        self.pos = self.add_vec(self.pos, self.multiply(self.speed * config.dt * slowvalue, self.v))
        if not self.killit:
            self.particle_system.add_particle(self.pos)
        self.rot_center()
        self.renderPosition(playerpos)
        self.rect.centerx = self.renderpos[0]
        self.rect.centery = self.renderpos[1]
        self.angle = self.calculate_angle(self.v)

