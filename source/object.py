import numpy as np

class Object:
    def __init__(self):
        self.pos = np.array([1.0,0.0])
        self.v = np.array([1.0,0.0])
        self.mass = 0
        self.speed = 10
        self.renderpos = np.array([0,0])

    def angle_2vec(self, a, b):
        dot = a.dot(b)
        mag_a = np.linalg.norm(a)
        mag_b = np.linalg.norm(b)
        t = dot / (mag_a * mag_b)
        return np.arccos(t)

    def renderPosition(self,ref):
        self.renderpos = self.pos - ref
        self.renderpos += np.array([300,300])

    def unit(self, x):
        return x / np.linalg.norm(x)
