import config
import math
import pygame as py
class Bullet(py.sprite.Sprite):
    def __init__(self,angle):
        py.sprite.Sprite.__init__(self)
        self.pos = [0,0]
        self.dir = [1,0]
        self.time = 5

        self.image = py.image.load("../images/bullet.png")

        self.rect = self.image.get_rect()
        self.speed  = 1500

        self.angle = angle
        self.rot_center()

    def rot_center(self):
        orig_rect = self.image.get_rect()
        # rad = np.arccos(np.dot(self.unit(self.v),np.array([1,0])))
        # self.angle = np.rad2deg(rad)
        rot_image = py.transform.rotate(self.image, -self.angle - 90)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.image = rot_image
        self.rect = self.image.get_rect()
        self.rect.centerx = config.screen_width / 2
        self.rect.centery = config.screen_height / 2

class BulletsSystem:
    def __init__(self):
        self.bullets = py.sprite.Group()
        self.nexttime = 1
        self.slowvalue = 1

    def add_bullet(self,pos,direction,angle):
        print("Calling",direction)
        if self.nexttime <0:
            if type(direction) == type([]):
                b = Bullet(angle)
                b.pos = list(pos)
                b.dir = dir
                self.bullets.add(b)
                print("Add1")
            elif type(direction) == type(2) or type(direction) == type(2.3):
                b =Bullet(angle)
                b.pos = list(pos)
                r = math.radians(direction)
                dire = [math.cos(r),math.sin(r)]
                b.dir = dire
                self.bullets.add(b)
                print("Add2")
            self.nexttime = 1
        else:
            self.nexttime -= 1*self.slowvalue
    def update(self,slowvalue):
        self.slowvalue = slowvalue
        print("Sprites",len(self.bullets.sprites()))
        for b in self.bullets.sprites():
            if b.time>0:
                b.pos[0] += b.dir[0]*b.speed*config.dt*slowvalue
                b.pos[1] += b.dir[1]*b.speed*config.dt*slowvalue
                b.time -= 0.5*slowvalue

            else:
                b.kill()




