
import math
import config

class Object:
    def __init__(self):
        self.pos = [1.0,0.0]
        self.v = [1.0,0.0]
        self.mass = 0
        self.speed = 10
        self.renderpos = [0,0]
        self.w_2 = config.screen_width/2
        self.h_2 = config.screen_height/2

    def norm(self,x):
        return math.sqrt(x[0]**2 + x[1]**2)

    def add_vec(self, a, b):
        return [a[0]+b[0],a[1]+b[1]]

    def sub_vec(self,a,b):
        return [a[0] - b[0], a[1] - b[1]]

    def multiply(self,cons,x):
        return [cons*x[0],cons*x[1]]

    def dot(self,a,b):
        return a[0]*b[0]+a[1]*b[1]

    def angle_2vec(self, a, b):
        dot = self.dot(a,b)
        mag_a = self.norm(a)
        mag_b = self.norm(b)
        t = dot / (mag_a * mag_b)
        if(t>1):
            return 0
        return math.acos(t)

    def renderPosition(self,ref,):
        self.renderpos = [self.pos[0] - ref[0],self.pos[1] - ref[1]]
        self.renderpos[0] += self.w_2
        self.renderpos[1] += self.h_2

    def unit(self, x):
        n = self.norm(x)
        if n!=0:
            return [x[0]/n,x[1]/n]
        else:
            return [0,0]

    def calculate_angle(self,x):
        n = self.norm(x)
        t = math.atan(x[1]/x[0])
        a = math.fabs(math.degrees(t))
        if x[0] >= 0:
            if x[1]>=0:
                return a
            else:
                return -a
        else:
            if x[1]>=0:
                return 180-a
            else:
                return a-180

