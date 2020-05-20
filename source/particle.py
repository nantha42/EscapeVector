import object
import config
import vectors

class Particle(object.Object):
    def __init__(self,pos):
        object.Object.__init__(self)
        self.pos = list(pos)
        self.size = 1

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

