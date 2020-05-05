import numpy as np
from object import Object
import particle
import config

class Player(Object):

    def __init__(self):
        Object.__init__(self)
        self.speed= 30
        self.turn_speed = 1.5

        self.particle_system = particle.ParticleSystem()

    def update(self,mousepos):
        dir = np.array(mousepos) - np.array((300,300))
        dir = self.unit(dir)

        self.v = self.v * self.speed + dir*self.turn_speed
        #self.v = dir
        self.v = self.unit(self.v)

        self.pos += self.v*self.speed * config.dt
        self.particle_system.add_particle(self.pos)

    def renderPosition(self,ref):
        self.particle_system.renderPosition(self.pos)
