import vectors
import random
class Brain:
    def __init__(self):
        self.fighters = []
        self.choosen = False
        self.choosen_fighter = None

    def control1(self,player):
        if not self.choosen:
            r = random.randint(0,len(self.fighters))
            self.choosen_fighter = self.fighters[r]
            self.choosen = True

        for i in range(len(self.fighters)):
            if self.choosen_fighter != self.fighters[i]:
                f = self.fighters[i]
                f.receive_signal(["maintaindistance"])


    def control(self,player):
        for i in range(len(self.fighters)):
            fa = self.fighters[i]
            fa.receive_signal(["noslowdown"])
            for j in range(len(self.fighters)):
                if i!=j:
                    fb = self.fighters[j]
                    if vectors.norm(vectors.sub_vec(fa.pos,fb.pos)) <450:
                        d1 = vectors.norm(vectors.sub_vec(fa.v,player.pos))
                        d2 = vectors.norm(vectors.sub_vec(fb.v,player.pos))
                        if d1 < d2:
                            #fa is closen
                            # print("Slos")
                            fb.receive_signal(["slowdown"])
                        else:
                            fa.receive_signal(["slowdown"])
                    else:
                        fa.receive_signal(["noslowdown"])
                        fb.receive_signal(["noslowdown"])
