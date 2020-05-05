import pygame as py
import numpy as np
import player
import missile

class Game:
    def __init__(self):
        self.win = py.display.set_mode((600,600))
        py.display.set_caption("EscapeVector")
        self.quit = False
        self.mouse_pos = (0,0)
        self.player = player.Player()
        self.player.pos = np.array([200,0],dtype=float)
        self.missile = missile.Missile()
        self.missile.pos = np.array([50,0],dtype=float)
        self.missile1 = missile.Missile()
        self.missile1.pos = np.array([100,25],dtype=float)

    def event_handler(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.quit = True

            if event.type == py.MOUSEMOTION:
                self.mouse_pos = py.mouse.get_pos()
            if event.type == py.MOUSEBUTTONDOWN:
                self.player.speed=50

            if event.type == py.MOUSEBUTTONUP:
                self.player.speed=30

    def draw(self):
        self.win.fill((30,0,40))
        py.draw.circle(self.win,(255,255,100),(300,300),5,5)
        print(self.missile.renderpos)
        py.draw.circle(self.win,(255,0,0),np.array(self.missile.renderpos,dtype=int),3,3)
        py.draw.circle(self.win, (255, 0, 0), np.array(self.missile1.renderpos, dtype=int), 3, 3)

        for i in self.missile.particle_system.particles:
            py.draw.circle(self.win, (100, 100, 0), np.array(i.renderpos, dtype=int), 2, 2)
        for i in self.player.particle_system.particles:
            py.draw.circle(self.win, (0, 255, 0), np.array(i.renderpos, dtype=int), 2, 2)
        for i in self.missile1.particle_system.particles:
            py.draw.circle(self.win, (100, 100, 0), np.array(i.renderpos, dtype=int), 2, 2)

    def update(self):
        self.player.update(self.mouse_pos)
        self.missile.update(self.player.pos)
        self.missile1.update(self.player.pos)
        self.player.renderPosition(np.array([0,0]))
        self.missile.renderPosition(self.player.pos)
        self.missile1.renderPosition(self.player.pos)
        py.display.update()


    def run(self):
        while not self.quit:

            self.event_handler()
            self.draw()
            self.update()

if __name__ == '__main__':
    g = Game()
    g.run()