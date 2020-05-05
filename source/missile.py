import object
import numpy as np
import particle
import config

class Missile(object.Object):

    def __init__(self):
        object.Object.__init__(self)
        self.speed = np.random.randint(40,45)
        self.particle_system = particle.ParticleSystem()
        self.turn_speed = 1.5
    def renderPosition(self,ref):
        super().renderPosition(ref)
        self.particle_system.renderPosition(ref)

    def update(self,playerpos):
        rot_dir = playerpos - self.pos
        unit_dir = rot_dir/np.linalg.norm(rot_dir)
        v_turn = self.unit(rot_dir - self.v)


        self.v = self.v*self.speed + v_turn*self.turn_speed
        self.v = self.unit(self.v)
        self.pos += self.v*self.speed*config.dt
        self.particle_system.add_particle(self.pos)

        # rotationAmount = np.cross(unit_dir,self.v)
        # pointout = self.unit(self.v) - np.array([1,0])
        # theta = self.angle_2vec(self.v)
        # perpen = np.array([-self.v[1],self.v[0]])
        # perpen_unit = np.array
