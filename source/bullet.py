import config
import math
class Bullet:
    def __init__(self):
        self.pos = [0,0]
        self.dir = [1,0]
        self.time = 10
        self.speed  = 2000

class BulletsSystem:
    def __init__(self):
        self.bullets = []

    def add_bullet(self,pos,direction):
        if type(direction) == type([]):
            b = Bullet()
            b.pos = list(pos)
            b.dir = dir
            self.bullets.append(b)
        elif type(direction) == type(2):
            b =Bullet()
            b.pos = list(pos)
            r = math.radians(direction)
            dire = [math.cos(r),math.sin(r)]
            b.dir = dire
            self.bullets.append(b)

    def update(self):
        remove = []
        for b in self.bullets:
            if b.time>0:
                b.pos[0] += b.dir[0]*b.speed*config.dt
                b.pos[1] += b.dir[1]*b.speed*config.dt
                b.time -= 0.5
            else:
                remove.append(b)

        for b in remove:
            print("removed bullet")
            self.bullets.remove(b)




