import pygame as py
import numpy as np
import player
import missile
import config
import explosion
import bullet
import random

class Game:
    def __init__(self):
        self.win = py.display.set_mode((config.screen_width, config.screen_height))
        py.display.set_caption("EscapeVector")
        self.quit = False
        self.mouse_pos = (0, 0)
        self.turn_right = False
        self.turn_left = False
        self.turbo = False
        self.throttle_down = True
        self.throttle_up = False
        self.clock = py.time.Clock()

        self.player = player.Player()
        self.explode = explosion.Explosion()
        self.player.pos = np.array([500, 0], dtype=float)

        self.bullets = bullet.BulletsSystem()
        self.shoot = False

        self.missile = missile.Missile()
        self.missile1 = missile.Missile()
        self.missile2 = missile.Missile()
        self.missile3 = missile.Missile()
        self.missile.pos = np.array([100, 500], dtype=float)
        self.missile1.pos = np.array([100, 125], dtype=float)
        self.missile2.pos = np.array([300, 125], dtype=float)
        self.missile3.pos = np.array([1000, 505], dtype=float)

        self.missiles = py.sprite.Group()
        self.explosions = []

        self.missiles.add(self.missile2)
        self.missiles.add(self.missile3)
        self.missiles.add(self.missile)
        self.missiles.add(self.missile1)
        self.dirty_rects = []

    def event_handler(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.quit = True

            if event.type == py.KEYDOWN:
                if event.key == py.K_a:
                    self.turn_left = True

                if event.key == py.K_d:
                    self.turn_right = True

                if event.key == py.K_w:
                    self.throttle_up = True
                    self.throttle_down = False

                if event.key == py.K_SPACE:
                    self.shoot = True

            if event.type == py.KEYUP:
                if event.key == py.K_a:
                    self.turn_left = False

                if event.key == py.K_d:
                    self.turn_right = False

                if event.key == py.K_w:
                    self.throttle_up = False
                    self.throttle_down = True

                if event.key == py.K_UP:
                    self.throttle_up = False

                if event.key == py.K_DOWN:
                    self.throttle_down = False

    def draw(self):
        self.win.fill((0x8c, 0xbe, 0xd6))
        # self.win.fill((0,0,0))
        # py.draw.circle(self.win,(255,255,100),(300,300),5,5)
        self.dirty_rects = []
        self.win.blit(self.player.image, self.player.rect)
        self.dirty_rects.append(self.player.rect)
        # py.draw.circle(self.win,(255,0,0),np.array(self.missile.renderpos,dtype=int),3,3)
        # py.draw.circle(self.win, (255, 0, 0), np.array(self.missile1.renderpos, dtype=int), 3, 3)

        self.missiles.draw(self.win)

        for missile in self.missiles.sprites():
            for i in missile.particle_system.particles:
                if (i.size < config.particle_expansion_size):
                    py.draw.circle(self.win, (100, 100, 100), np.array(i.renderpos, dtype=int), int(i.size),
                                   int(i.size))
                    # self.dirty_rects.append()
                    i.size += .1
        for i in self.player.particle_system.particles:
            if (i.size < config.particle_expansion_size):
                py.draw.circle(self.win, (100, 100, 100), np.array(i.renderpos, dtype=int), int(i.size), int(i.size))
                i.size += .1

        self.draw_explosions()
        self.draw_missile_fuel_indicator()
        self.draw_hud()
        self.draw_bullets()

    def draw_explosions(self):
        expired = []
        for exp in self.explosions:
            pos = exp[0]
            img = None
            if (exp[1] < 11):

                img = self.explode.get_image(int(exp[1]))
                rect = img.get_rect()
                pos = pos - self.player.pos + (config.screen_width / 2, config.screen_height / 2) - (
                rect.w / 2, rect.h / 2)
                self.win.blit(img, np.array(pos, dtype=int))
                exp[1] += .5
            else:
                expired.append(exp)

        for exp in expired:
            self.explosions.remove(exp)

    def makeint(self, arr):
        return np.array(arr, dtype=int)

    def draw_missile_fuel_indicator(self):
        for missile in self.missiles.sprites():
            if missile.killit == False:
                f = missile.fuel
                rect = missile.rect
                prepos = [rect.x, rect.y]
                pospos = [rect.x, rect.y]

                pospos[0] += 32 * (f / config.missile_fuel)

                py.draw.line(self.win, (0, 255, 0), self.makeint(prepos), self.makeint(pospos), 3)

    def draw_hud(self):
        self.draw_player_throttle()

    def draw_player_throttle(self):
        throttle = self.player.speed
        x = config.screen_width - 40
        y = config.screen_height - 100
        w = 30
        h = (throttle / config.normal_speed) * 80
        py.draw.rect(self.win, (255, 255, 30), py.Rect((x, y + (80 - h), w, h)), 0)

    def detect_collisions(self):
        for missile in self.missiles.sprites():
            col = py.sprite.collide_mask(missile, self.player)
            if col != None:
                missile.killit = True
                self.explosions.append([missile.pos, 0])

        group = self.missiles.sprites()
        for i in range(len(group)):
            missile = group[i]
            for j in range(i, len(group)):
                missileB = group[j]
                if missile != missileB:
                    if py.sprite.collide_mask(missile, missileB) != None:
                        missile.killit = True
                        missileB.killit = True
                        self.explosions.append([missile.pos, 0])
                        self.explosions.append([missileB.pos, 0])

    def draw_bullets(self):
        w = config.screen_width / 2
        h = config.screen_height / 2

        for b in self.bullets.bullets:
            x = b.pos[0] - self.player.pos[0] + w
            y = b.pos[1] - self.player.pos[1] + h
            l = 80
            x1 = (b.pos[0] - b.dir[0] * l) - self.player.pos[0] + w
            y1 = (b.pos[1] - b.dir[1] * l) - self.player.pos[1] + h

            print([x, y], [x1, y1])
            py.draw.line(self.win, (255, 100, 0), [x, y], [x1, y1], 3)

    def update(self):

        if self.shoot:
            self.shoot = False

            self.bullets.add_bullet(self.player.pos, self.player.angle+random.randint(-5,5))

        if self.turn_left:
            self.player.turn_left()
        if self.turn_right:
            self.player.turn_right()

        if self.throttle_up:
            self.player.throttleUp()

        if self.throttle_down:
            self.player.throttleDown()

        self.player.update(self.mouse_pos)
        for missile in self.missiles.sprites():
            missile.update(self.player.pos, self.player.speed)
            if missile.fuel < 0 and missile.killit == False:
                missile.killit = True
                self.explosions.append([missile.pos, 0])

        self.player.renderPosition(np.array([0, 0]))
        self.detect_collisions()
        self.bullets.update()
        py.display.update()

    def run(self):
        avg = 0
        count = 0
        while not self.quit:
            self.event_handler()
            self.draw()
            self.update()
            avg += self.clock.tick(40)
            count += 1


if __name__ == '__main__':
    g = Game()
    g.run()
