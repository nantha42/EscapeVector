import pygame as py
import time

class Sound:
    def __init__(self):
        self.songs = ["../sounds/explosion01.wav","../sounds/shootbullet.wav","../sounds/tick1.wav","../sounds/gametrack3.wav","../sounds/bullethit.wav","../sounds/explosion.wav"]
        py.mixer.init()
        self.boom = py.mixer.Sound(self.songs[0])
        self.shoot = py.mixer.Sound(self.songs[1])
        self.tick = py.mixer.Sound(self.songs[2])
        self.serious = py.mixer.Sound(self.songs[3])
        self.hit = py.mixer.Sound(self.songs[4])
        self.missile_explosion = py.mixer.Sound(self.songs[5])
        self.sound = 0.1
        self.boomtimer = time.time()
        self.shoottimer = time.time()
        self.lasttick = time.time()

    def playTheme(self):
        self.serious.set_volume(0.5)
        self.serious.play(-1)


    def mBooms(self):
        now  = time.time()
        if now -self.boomtimer > 2:

            self.boom.set_volume(0.5)
            self.boom.play(0)
            self.boomtimer= time.time()

    def mShoots(self):
        self.shoot.set_volume(self.sound)
        self.shoot.play(0)

    def mHit(self):
        self.hit.set_volume(self.sound)
        self.hit.play(0)

    def missileExplosion(self,dis):
        v = 1
        if dis<100:
            v = 0.5
        elif dis < 300:
            v = 0.4
        elif dis < 700:
            v = 0.25
        elif dis < 1000:
            v = 0.17
        elif dis < 2000:
            v = 0.1
        self.missile_explosion.set_volume(v)
        self.missile_explosion.play(0)

    def mTicks(self,tickdur):
        now = time.time()
        if now-self.lasttick > tickdur:
            self.tick.set_volume(0.3)
            self.tick.play(0)
            self.lasttick = now
            return now
        return -1