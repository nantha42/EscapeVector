import pygame as py
import time


class Sound:
    def __init__(self):
        self.songs = ["../sounds/explosion01.wav","../sounds/shootbullet.wav","../sounds/tick1.wav","../sounds/gametrack.wav","../sounds/bullethit.wav"]
        py.mixer.init()
        self.boom = py.mixer.Sound(self.songs[0])
        self.shoot = py.mixer.Sound(self.songs[1])
        self.tick = py.mixer.Sound(self.songs[2])
        self.serious = py.mixer.Sound(self.songs[3])
        self.hit = py.mixer.Sound(self.songs[4])
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
            print(now,self.boomtimer,now-self.boomtimer)
            self.boom.set_volume(self.sound)
            self.boom.play(0)
            self.boomtimer= time.time()

    def mShoots(self):
        self.shoot.set_volume(self.sound)
        self.shoot.play(0)

    def mHit(self):
        self.hit.set_volume(self.sound)
        self.hit.play(0)

    def mTicks(self,tickdur):
        now = time.time()
        if now-self.lasttick > tickdur:
            self.tick.set_volume(0.3)
            self.tick.play(0)
            self.lasttick = now
            return now
        return -1
