import numpy as np
import object

class Particle(object.Object):
    def __init__(self,pos):
        object.Object.__init__(self)
        self.pos = np.array(pos)


class ParticleSystem:
    def __init__(self):
        self.particles = []
        self.particle_release_time = 0
        self.particle_limits = 100

    def add_particle(self,pos):
        self.particle_release_time += 1
        if self.particle_release_time > 10:
            print(self.particle_release_time)
            self.particles.append(Particle(pos))
            self.particle_release_time = 0

        if len(self.particles) > self.particle_limits:
            self.particles.pop(0)

    def renderPosition(self, ref):
        for p in self.particles:
            p.renderPosition(ref)



