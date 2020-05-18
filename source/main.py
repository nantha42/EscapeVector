import pygame as py
import player
import missile
import config
import explosion
import fighter
import bullet
import random
import vectors
import minimap


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
        self.slowtime = False


        self.slowduration = 10


        self.clock = py.time.Clock()

        self.hud_base = py.transform.scale(py.image.load("../images/hud.png"), (200, 200))
        self.player = player.Player()
        self.explode = explosion.Explosion()
        self.player.pos = [500, 0]
        self.minimap = minimap.Minimap()

        self.fighter = fighter.Fighter()
        self.fighter1 = fighter.Fighter()
        self.missiles = py.sprite.Group()
        self.fighters = py.sprite.Group()
        self.slowvalue = 1

        self.fighter.launched_missiles = self.missiles
        # self.fighter1a.launched_missiles = self.missiles
        self.fighter.pos = [150.0, 0]
        # self.fighter1.pos = [10.0, 500]
        self.fighters.add(self.fighter)
        # self.fighters.add(self.fighter1)

        self.fighter.otherFighters = self.fighters
        # self.fighter1.otherFighters = self.fighters
        self.bullets = bullet.BulletsSystem()
        self.shoot = False

        self.explosions_size = 10
        self.initial_explosion = []

        self.explosions = []

        self.dirty_rects = []

    def get_exp(self, pos):
        return [pos, 0, 10, 0, 10]

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

                if event.key == py.K_n:
                    self.turbo = True

                if event.key == py.K_j:
                    self.slowtime = True

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

                if event.key == py.K_SPACE:
                    self.shoot = False

                if event.key == py.K_n:
                    self.turbo = False

                if event.key == py.K_j:
                    self.slowtime = False

    def draw(self):
        self.win.fill((0x8c, 0xbe, 0xd6))
        self.dirty_rects = []
        self.draw_bullets()
        if self.player.health > 0:
            self.win.blit(self.player.image, self.player.rect)

        self.missiles.draw(self.win)
        self.fighters.draw(self.win)

        for missile in self.missiles.sprites():
            for i in missile.particle_system.particles:
                if (i.size < config.particle_expansion_size):
                    py.draw.circle(self.win, (100, 100, 100), vectors.ret_int(i.renderpos), int(i.size),
                                   int(i.size))

                    i.size += .1
        for i in self.player.particle_system.particles:
            if (i.size < config.particle_expansion_size):
                py.draw.circle(self.win, (100, 100, 100), vectors.ret_int(i.renderpos), int(i.size), int(i.size))
                i.size += .1
        # for i in self.player.vParticle_system.particles:
        #     py.draw.circle(self.win, (255, 255, 255), vectors.ret_int(i.renderpos), 1, 1)
        self.win.blit(self.minimap.image, (30, config.screen_height - 128))
        self.draw_explosions()
        self.draw_missile_fuel_indicator()
        self.draw_fighter_health()
        self.draw_hud()


    def draw_explosions(self):
        expired = []
        for exp in self.explosions:
            pos = exp[0]
            img = None
            if (exp[2] < 500):
                img = self.explode.get_image(0)
                rect = img.get_rect()
                pos = vectors.sub_vec(vectors.add_vec(vectors.sub_vec(pos, self.player.pos),
                                                      [config.screen_width / 2, config.screen_height / 2]), (
                                          rect.w / 2, rect.h / 2))
                if (exp[1] < 11):
                    img = self.explode.get_image(int(exp[1]))

                    self.win.blit(img, vectors.ret_int(pos))
                    exp[1] += .5*self.slowvalue

                newpos = vectors.ret_int([pos[0] + rect.w / 2, pos[1] + rect.h / 2])
                # print(newpos)
                if exp[4] > 1:
                    py.draw.circle(self.win, (120, 120, 120), newpos, int(exp[2]), int(exp[4]))
                    py.draw.circle(self.win, (120, 120, 120), newpos, int(1.3 * exp[2]), 1)

                if (exp[3] < 15):
                    exp[3] += 0.5*self.slowvalue
                exp[4] -= 0.7*self.slowvalue
                exp[2] += (30 - exp[3])*self.slowvalue

            else:
                expired.append(exp)

        for exp in expired:
            self.explosions.remove(exp)

    def makeint(self, arr):
        return vectors.ret_int(arr)

    def draw_missile_fuel_indicator(self):
        for missile in self.missiles.sprites():
            if missile.killit == False:
                f = missile.fuel
                rect = missile.rect
                prepos = [rect.x, rect.y]
                pospos = [rect.x, rect.y]

                pospos[0] += 32 * (f / config.missile_fuel)

                py.draw.line(self.win, (0, 255, 0), self.makeint(prepos), self.makeint(pospos), 3)

    def draw_fighter_health(self):
        if not self.fighter.killit:
            f = self.fighter.health
            rect = self.fighter.rect
            prepos = [rect.x, rect.y]
            pospos = [rect.x, rect.y]

            pospos[0] += 90 * (f / 100)
            py.draw.line(self.win, (0, 255, 0), self.makeint(prepos), self.makeint(pospos), 3)

    def draw_hud(self):
        self.draw_player_health()
        self.draw_player_throttle()

    def draw_player_health(self):
        hudbase = self.hud_base.copy()
        hud_size = 2
        x = 17 * hud_size
        y = 17 * hud_size
        if self.player.health > 0:
            w = (self.player.health / config.player_health) * 77 * hud_size
        else:
            w = 1
        h = 5 * hud_size
        py.draw.rect(hudbase, (153, 229, 80), py.Rect((x, y, w, h)), 0)
        x = 17 * hud_size
        y = 29 * hud_size
        if self.player.turbo > 0:
            w = (self.player.turbo / 100) * 61 * hud_size
        else:
            w = 1
        h = 7 * hud_size
        py.draw.rect(hudbase, (99, 155, 255), py.Rect((x, y, w, h)), 0)
        self.win.blit(hudbase, (10, 10))

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
                self.explosions.append(self.get_exp(missile.pos))
                self.player.health -= 30
                self.player.damaging = True
                if self.player.health <= 0:
                    self.explosions.append(self.get_exp(self.player.pos))
                    # self.player.kill()
                    self.player.live = False
                    self.bullets.bullets.empty()

        for ship in self.fighters.sprites():
            j =py.sprite.collide_mask(ship,self.player)
            if j!=None :
                ship.kill()
                self.player.health = 0
                j = list(j)
                self.explosions.append(self.get_exp(self.player.pos))
                self.explosions.append(self.get_exp(ship.pos))
                print("J ",j)


        group = self.missiles.sprites()
        bulls = self.bullets.bullets.sprites()
        for i in range(len(group)):
            missile = group[i]
            for j in range(i, len(group)):
                missileB = group[j]
                if missile != missileB:
                    if py.sprite.collide_mask(missile, missileB) != None:
                        missile.killit = True
                        missileB.killit = True
                        self.explosions.append(self.get_exp(missile.pos))
            hitted_bullets = []
            for j in range(i, len(bulls)):
                b = bulls[j]
                if py.sprite.collide_mask(b, missile):
                    missile.killit = True
                    self.explosions.append(self.get_exp(missile.pos))
                    hitted_bullets.append(b)

                if py.sprite.collide_mask(b,self.fighter):
                    self.fighter.health -= 10
                    hitted_bullets.append(b)
                    if self.fighter.health<=0:
                        self.fighter.killit = True
                        self.explosions.append(self.get_exp(self.fighter.pos))
            for b in hitted_bullets:
                b.kill()
    def draw_bullets(self):
        w = config.screen_width / 2
        h = config.screen_height / 2

        for b in self.bullets.bullets:
            k = random.randint(0, 80)
            b.rect.centerx = (b.pos[0] - b.dir[0] * k) - self.player.pos[0] + w
            b.rect.centery = (b.pos[1] - b.dir[1] * k) - self.player.pos[1] + h
            # print("Drawing",b.rect.x,b.rect.y)
            self.win.blit(b.image, b.rect)

    def handle_events(self):
        if self.shoot and self.player.live:

            self.bullets.add_bullet(self.player.pos, self.player.angle + random.randint(-2, 2), self.player.angle)

        if self.turn_left:
            self.player.turn_left()

        if self.turn_right:
            self.player.turn_right()

        if self.throttle_up:
            self.player.throttleUp()

        if self.throttle_down:
            self.player.throttleDown()

        if self.turbo:
            self.player.release_turbo()
        else:
            self.player.stop_turb()

    def update(self):
        if self.slowtime:
            self.slowvalue = 0.3
        else:
            self.slowvalue = 1
        self.handle_events()
        self.player.update(self.slowvalue)
        self.fighters.update(self.player.pos, self.player.speed,self.slowvalue)
        for missile in self.missiles.sprites():
            missile.update(self.player.pos, self.player.speed,self.slowvalue)
            if missile.fuel < 0 and missile.killit == False:
                missile.killit = True
                self.explosions.append(self.get_exp(missile.pos))
        all_sprites = []
        if self.fighter.killit == False:
            all_sprites = [self.fighter]
        all_sprites.extend(self.missiles.sprites())
        self.minimap.update(all_sprites, self.player)
        self.player.renderPosition()
        self.detect_collisions()
        self.bullets.update(self.slowvalue)
        py.display.update()

    def run(self):
        avg = 0
        count = 0
        while not self.quit:
            self.event_handler()
            self.draw()
            self.update()

            self.clock.tick(40)


if __name__ == '__main__':
    g = Game()
    g.run()
