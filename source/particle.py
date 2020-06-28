import object
import config
import vectors
import random
import math

class Particle(object.Object):
    def __init__(self,pos):
        object.Object.__init__(self)
        self.pos = list(pos)
        self.size = 1

class Colored_Particle(object.Object):
    def __init__(self,pos):
        object.Object.__init__(self)
        self.pos = list(pos)
        self.size = 1

class SparkSystem:
    def __init__(self):
        self.particles = []

    def add_particles(self,pos, vel,n):
        for i in range(n):
            d = random.randint(5,10)
            angle = random.randint(0,359)
            color  = None
            if(random.randint(0,1)):
                color = [0xff,0xdf,0x00]
            else:
                color = [0xdd,0x00,0x00]
            smp = object.Object()
            angle = smp.calculate_angle(vel)

            a1 = int(angle - 175)%360
            a2 = int(angle + 175)%360
            #print(min(a1%360,a2%360),max(a1%360,a2%360))
            a = math.radians(random.randint(min(a1, a2), max(a1, a2)))
            np_angle = math.radians(random.randint(min(a1, a2), max(a1, a2)))
            newpoint = [math.cos(np_angle) * d, math.sin(np_angle) * d]
            #print(a1,a2)
            newpoint = smp.add_vec(pos,newpoint)
            speed = random.randint(100,500)
            v = [math.cos(a),math.sin(a)]
            self.particles.append([newpoint,v, color,100,speed])

    def update(self,slowvalue):
        removethis = []
        for p in self.particles:
            pos = p[0]
            v = p[1]
            pos[0] += v[0]*config.dt*slowvalue*p[-1]
            pos[1] += v[1]*config.dt*slowvalue*p[-1]
            p[3]-=1
            if(p[3]<0):
                removethis.append(p)
        for p in removethis:
            self.particles.remove(p)


class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.particle_release_time = 0
        self.particle_limits = 50

    def add_particle(self,pos):
        self.particle_release_time += 1
        if self.particle_release_time > 10:

            self.particles.append(Particle(pos))
            self.particle_release_time = 0

        if len(self.particles) > self.particle_limits:
            self.particles.pop(0)

    def renderPosition(self, ref,):
        for p in self.particles:
            p.renderPosition(ref)


class VelocityParticleSystem:
    def __init__(self):
        self.particles = []
        self.particle_release_time = 3
        self.particle_limits = 50

    def add_particle(self,pos,vel):


        parti = Particle(pos)
        parti.v = vel
        self.particles.append(parti)
        self.particle_release_time = 0

        if len(self.particles) > self.particle_limits:
            self.particles.pop(0)

    def update(self,slowvalue):
        for p in self.particles:
            p.pos = vectors.add_vec(p.pos,vectors.multiply(config.dt*slowvalue,p.v))


    def renderPosition(self, ref,slowvalue):
        self.update(slowvalue)
        for p in self.particles:
            p.renderPosition(ref)

if __name__ == '__main__':
    j = object.Object()
    # print(j.calculate_angle([23,34]))
