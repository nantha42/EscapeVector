import pygame as py
import math
import vectors
import config
import random

class Clouds:
    def __init__(self):
        self.cloud_imgs = []
        self.scale = 700
        for i in range(1,14):
            img = py.image.load("../images/clouds/cloud"+str(i)+".png")
            img = py.transform.scale(img,(self.scale,self.scale))
            self.cloud_imgs.append(img)


    def draw(self,win,pos):

        if pos[0] < 0:
            qx = int(pos[0]/self.scale -1)
        else:
            qx = int(pos[0] / self.scale )
        if pos[1] < 0:
            qy = int(pos[1]/self.scale - 1)
        else:
            qy = int(pos[1] / self.scale )

        i = math.fabs(qx+qy)%13
        xys = [[qx*self.scale, qy*self.scale, i]]


        lqx = qx-1
        lqy = qy
        l = math.fabs(lqx + lqy) % 13
        xys.append([lqx*self.scale,lqy*self.scale,l])

        lqx = qx - 1
        lqy = qy-1
        l = math.fabs(lqx + lqy) % 13
        xys.append([lqx * self.scale, lqy * self.scale, l])

        lqx = qx + 1
        lqy = qy - 1
        l = math.fabs(lqx + lqy) % 13
        xys.append([lqx * self.scale, lqy * self.scale, l])

        rqx = qx+1
        rqy = qy
        r = math.fabs(rqx + rqy) % 13
        xys.append([rqx*self.scale, rqy*self.scale, r])

        rqx = qx + 1
        rqy = qy+1
        r = math.fabs(rqx + rqy) % 13
        xys.append([rqx * self.scale, rqy * self.scale, r])

        rqx = qx - 1
        rqy = qy + 1
        r = math.fabs(rqx + rqy) % 13
        xys.append([rqx * self.scale, rqy * self.scale, r])

        uqx = qx
        uqy = qy-1
        u = math.fabs(uqx + uqy) % 13
        xys.append([uqx*self.scale, uqy*self.scale, u])

        dqx = qx
        dqy = qy+1
        d = math.fabs(dqx + dqy) % 13
        xys.append([dqx*self.scale, dqy*self.scale, d])

        for xy in xys:
            ind = int(xy[2])
            random.seed(xy[0]*xy[1]+xy[1])
            c = random.randint(0,1)
            if c==1:
                g = vectors.sub_vec([xy[0],xy[1]],pos)
                g = vectors.add_vec(g,[config.screen_width/2,config.screen_height/2])
                g = vectors.ret_int(g)
                win.blit(self.cloud_imgs[ind],g)
