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
import sound
import time
import brain
import menu
import clouds
import emp
import particle

class Game:
    def __init__(self):
        self.win = py.display.set_mode((config.screen_width, config.screen_height))
        py.font.init()
        py.display.set_caption("EscapeVector")

        #----------Menusystem---------
        self.menu_system = menu.Menu()

        ############
        self.mouse_clicked = False
        self.quit = False
        self.mouse_pos = (0, 0)
        self.pressed_escape = False
        self.turn_right = False
        self.turn_left = False
        self.turbo = False
        self.throttle_down = True
        self.throttle_up = False
        self.slowtime = False
        self.slowduration = 10
        self.clock = py.time.Clock()
        self.hud_base = py.transform.scale(py.image.load("../images/hud.png"), (200, 200))

        self.explode = explosion.Explosion()

        self.minimap = minimap.Minimap()
        self.missiles_exploded = []
        self.fighters = py.sprite.Group()
        self.missiles = py.sprite.Group()
        self.emps = py.sprite.Group()
        self.turn_screen_red = False
        self.slowvalue = 1
        self.bullets = bullet.BulletsSystem()
        self.enemiesbullets = bullet.BulletsSystem()
        self.shoot = False
        self.ai = brain.Brain()
        self.ai.fighters = self.fighters.sprites()
        self.sparkSystem = particle.SparkSystem()
        self.explosions_size = 10
        self.initial_explosion = []
        self.clouds = clouds.Clouds()
        self.explosions = []

        self.screen_r = 0x8c
        self.screen_g = 0xbe
        self.screen_b = 0xd6
        self.turn_screen_normal = True

        self.dirty_rects = []
        self.game_exists = False
        #######sounds#####
        self.sounds = sound.Sound()
        self.playerhit = False
        self.fighterhit = False
        self.ticklowspeed = 0.5
        self.tickhighspeed = 0.1
        self.tickspeedrate = 0.05
        self.tickspeed = 0.1

    def initiate_game(self):
        level = self.menu_system.level_selected
        leveldata = self.menu_system.database.leve_loader.get_Level(level)

        for i in range(leveldata[0]):
            figh = fighter.Fighter()
            figh.launched_missiles = self.missiles
            self.fighters.add(figh)
            figh.otherFighters = self.fighters
            figh.pos = [(i+1)*-400,(i+1)*231]

        for i in range(leveldata[1]):
            figh = fighter.EmpFighter()
            self.fighters.add(figh)
            figh.active_emp = self.emps
            figh.otherFighters = self.fighters
            figh.pos = [(i+1)*-800,(i+1)*-400]

        self.player = player.Player()
        self.player.pos = [500, 0]

    def get_exp(self, pos):
        return [pos, 0, 10, 0, 10]

    def event_handler(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                self.menu_system.state = "quitgame"

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

                if event.key == py.K_LSHIFT:
                    self.turbo = True

                if event.key == py.K_j:
                    self.slowtime = True

                if event.key == py.K_ESCAPE:
                    self.pressed_escape = True
                    # print("Escape")

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

                if event.key == py.K_LSHIFT:
                    self.turbo = False

                if event.key == py.K_j:
                    self.slowtime = False

            if event.type == py.MOUSEBUTTONDOWN:
                self.mouse_clicked = True

            if event.type == py.MOUSEBUTTONUP:
                self.mouse_clicked = False

    def draw(self):
        if self.menu_system.state=="start" and self.game_exists:
            #print(self.turn_screen_red)
            if not self.turn_screen_red:
                self.win.fill((0x8c, 0xbe, 0xd6))
            else:
                self.win.fill((self.screen_r,self.screen_g,self.screen_b))
                color_change_perstep = 20
                if(self.screen_r+color_change_perstep<250 and not self.turn_screen_normal):
                    self.screen_r+=color_change_perstep
                    self.screen_b-=color_change_perstep
                    self.screen_g-=color_change_perstep

                else:
                    self.turn_screen_normal = True

                if(self.turn_screen_normal):
                    if(self.screen_r>140):
                        self.screen_r -= color_change_perstep
                        self.screen_b += color_change_perstep
                        self.screen_g += color_change_perstep
                    else:
                        self.turn_screen_red = False
            self.dirty_rects = []
            self.draw_bullets()

            if self.player.health > 0:
                self.win.blit(self.player.image, self.player.rect)

            self.missiles.draw(self.win)
            self.fighters.draw(self.win)

            # px = py.PixelArray(self.win)
            # for i in range(100):
            #     for j in range(100):
            #         px[i,j] = (255,0,0)
            # px.close()
            #
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

            self.draw_explosions()
            self.draw_missile_fuel_indicator()
            self.draw_fighter_health()
            self.draw_clouds()
            self.draw_hud()
            self.draw_emps()
            self.draw_sparks()

            self.win.blit(self.minimap.image, (30, config.screen_height - 128))
        else:
            self.menu_system.draw(self.win)

    def draw_sparks(self):
        #pxarray = py.PixelArray(self.win)
        for p in self.sparkSystem.particles:
            x,y = p[0][0]-self.player.pos[0]+config.screen_width/2,p[0][1]-self.player.pos[1]+config.screen_height/2
            if(random.randint(0,1)):
                self.win.fill(p[2],((x,y),(1,4)))
            else:
                self.win.fill(p[2], ((x, y), (4, 1)))
            #py.draw.circle(self.win,p[2],(x,y),1,1)
            #pxarray[x,y] = p[2]
            #print(x,y,p[2])
        #pxarray.close()
        # print(len(self.sparkSystem.particles))
        #print(pxarray)

    def draw_emps(self):
        self.emps.draw(self.win)

    def draw_clouds(self):
        self.clouds.draw(self.win,self.player.pos)

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
                    exp[1] += .5 * self.slowvalue
                newpos = vectors.ret_int([pos[0] + rect.w / 2, pos[1] + rect.h / 2])
                # print(newpos)
                if exp[4] > 1:
                    py.draw.circle(self.win, (120, 120, 120), newpos, int(exp[2]), int(exp[4]))
                    py.draw.circle(self.win, (120, 120, 120), newpos, int(1.3 * exp[2]), 1)

                if (exp[3] < 15):
                    exp[3] += 0.5 * self.slowvalue
                exp[4] -= 0.7 * self.slowvalue
                exp[2] += (30 - exp[3]) * self.slowvalue
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
        for fighter in self.fighters.sprites():
            if not fighter.killit:
                f = fighter.health
                rect = fighter.rect
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
            if not missile.activated:
                continue
            col = py.sprite.collide_mask(missile, self.player)
            if col != None:
                missile.killit = True
                self.missiles_exploded.append(vectors.norm(vectors.sub_vec(missile.pos,self.player.pos)))
                self.explosions.append(self.get_exp(missile.pos))
                self.player.health -= 30
                self.player.damaging = True
                self.turn_screen_red = True
                self.turn_screen_normal = False

                if self.player.health <= 0:
                    self.explosions.append(self.get_exp(self.player.pos))
                    self.player.live = False
                    self.bullets.bullets.empty()

            for fighter in self.fighters.sprites():
                if py.sprite.collide_mask(missile,fighter):
                    missile.killit = True
                    self.missiles_exploded.append(vectors.norm(vectors.sub_vec(missile.pos,self.player.pos)))
                    self.explosions.append(self.get_exp(missile.pos))
                    fighter.health-= 10

        #enemy player collision
        if self.player.live:
            for ship in self.fighters.sprites():
                j = py.sprite.collide_mask(ship, self.player)
                if j != None :
                    ship.kill()
                    self.player.health = 0
                    j = list(j)
                    self.missiles_exploded.append(0)
                    self.explosions.append(self.get_exp(self.player.pos))
                    self.explosions.append(self.get_exp(ship.pos))

        group = self.missiles.sprites()
        bulls = self.bullets.bullets.sprites()
        ebulls = self.enemiesbullets.bullets.sprites()
        hitted_bullets = []
        #missile missile collision
        for i in range(len(group)):
            missile = group[i]
            for j in range(i, len(group)):
                missileB = group[j]
                if missile != missileB:
                    if py.sprite.collide_mask(missile, missileB) != None:
                        missile.killit = True
                        missileB.killit = True
                        self.missiles_exploded.append(vectors.norm(vectors.sub_vec(missile.pos, self.player.pos)))
                        self.explosions.append(self.get_exp(missile.pos))

            #bullet missile collision
            for j in range(i, len(bulls)):
                b = bulls[j]
                if py.sprite.collide_mask(b, missile):
                    missile.killit = True
                    self.missiles_exploded.append(vectors.norm(vectors.sub_vec(missile.pos,self.player.pos)))
                    self.explosions.append(self.get_exp(missile.pos))
                    hitted_bullets.append(b)
                # bullet fighter collision

        for b in bulls:
            for fighter in self.fighters.sprites():
                if py.sprite.collide_mask(b, fighter) and not fighter.killit:
                    fighter.health -= 10
                    hitted_bullets.append(b)
                    self.fighterhit = True
                    self.sparkSystem.add_particles(b.pos,fighter.v,25)
                    if fighter.health <= 0:
                        fighter.killit = True
                        self.missiles_exploded.append(vectors.norm(vectors.sub_vec(fighter.pos,self.player.pos)))
                        self.explosions.append(self.get_exp(fighter.pos))

        if self.player.live:
            for b in ebulls:
                if py.sprite.collide_mask(b, self.player):
                    self.player.health -= 10
                    self.sparkSystem.add_particles(b.pos,b.dir,20)
                    self.turn_screen_red = True
                    self.turn_screen_normal = False
                    hitted_bullets.append(b)
                    self.playerhit = True
                    if self.player.health <= 0:
                        self.player.health = 0
                        self.missiles_exploded.append(0)
                        self.explosions.append(self.get_exp(self.player.pos))

            for b in hitted_bullets:
                b.kill()

        for emp in self.emps.sprites():
            if py.sprite.collide_mask(emp,self.player):
                self.player.emp_affected = True
                emp.kill()

    def draw_bullets(self):
        w = config.screen_width / 2
        h = config.screen_height / 2

        for b in self.bullets.bullets:
            k = random.randint(0, 80)
            b.rect.centerx = (b.pos[0] - b.dir[0] * k) - self.player.pos[0] + w
            b.rect.centery = (b.pos[1] - b.dir[1] * k) - self.player.pos[1] + h
            # print("Drawing",b.rect.x,b.rect.y)
            self.win.blit(b.image, b.rect)

        for b in self.enemiesbullets.bullets:
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

    def check_level_completed(self):
        if len(self.missiles.sprites())==0 and len(self.fighters.sprites())==0 and len(self.emps.sprites())==0 and len(self.enemiesbullets.bullets.sprites())==0 and len(self.explosions)==0:
            if self.menu_system.database.levelunlocked == self.menu_system.level_selected:
                self.menu_system.database.update_level()
            self.menu_system.state = "level_finished"

    def update(self):

        if self.menu_system.state == "start" and not self.pressed_escape:
            if not self.game_exists:
                self.initiate_game()
                self.game_exists = True

            self.check_level_completed()

            if self.slowtime:
                if self.slowvalue > 0.3:
                    self.slowvalue -= 0.04
            else:
                if self.slowvalue < 1:
                    self.slowvalue += 0.01

            self.handle_events()
            self.ai.control(self.player)
            self.player.update(self.slowvalue)
            self.fighters.update(self.player.pos, self.player.speed, self.slowvalue,self.player.live)
            for missile in self.missiles.sprites():
                missile.update(self.player.pos, self.player.speed, self.slowvalue)
                if missile.fuel < 0 and missile.killit == False:
                    missile.killit = True
                    self.explosions.append(self.get_exp(missile.pos))
            all_sprites = []
            all_sprites.extend(self.missiles.sprites())
            all_sprites.extend(self.fighters.sprites())
            self.minimap.update(all_sprites, self.player)
            self.player.renderPosition()
            self.detect_collisions()
            self.bullets.update(self.slowvalue)

            for f in self.fighters.sprites():
                if f.shoot:
                    # print(f.shoot)
                    if isinstance(f,fighter.EmpFighter):
                        if(len(self.emps.sprites())==0):
                            self.emps.add(emp.Emp(f.v,f.pos))
                    else:
                        self.enemiesbullets.add_bullet(f.pos, f.angle + random.randint(-2, 2), f.angle)
            self.enemiesbullets.update(self.slowvalue)
            self.emps.update(self.player.pos,self.slowvalue)
            self.sparkSystem.update(self.slowvalue)
            if self.player.health<=0:
                self.player.live = False
            self.playSounds()
        else:
            if self.game_exists and not self.pressed_escape and self.menu_system.option_selected!="gamemenu" and self:
                # print(self.menu_system.state)
                self.fighters.empty()
                self.missiles.empty()
                self.bullets.bullets.empty()
                self.enemiesbullets.bullets.empty()
                self.game_exists = False

            self.menu_system.update(py.mouse.get_pos(),self.mouse_clicked,self.pressed_escape)
            self.pressed_escape = False
        py.display.update()

    def playSounds(self):
        if self.player.speed >= 320 and self.player.speed <= 324 and self.player.live:
            self.sounds.mBooms()
        if len(self.missiles_exploded)>0:
            a = self.missiles_exploded[0]
            self.missiles_exploded.pop(0)
            self.sounds.missileExplosion(a)

        if self.shoot and self.player.live:
            if self.slowtime:
                now = time.time()
                if now - self.player.shoottimer >= 0.1*1.5:
                    self.sounds.mShoots()
                    self.player.shoottimer = now
            else:
                now = time.time()
                if now - self.player.shoottimer >= 0.1 :
                    self.sounds.mShoots()
                    self.player.shoottimer = now

        for fighte in self.fighters.sprites():

            if fighte.shoot and not isinstance(fighte,fighter.EmpFighter):
                if self.slowtime:
                    now = time.time()
                    if now - fighte.shoottimer >= 0.1 * 1.5:
                        self.sounds.mShoots()
                        fighte.shoottimer = now
                else:
                    now = time.time()
                    if now - fighte.shoottimer >= 0.1:
                        self.sounds.mShoots()
                        fighte.shoottimer = now

        if self.slowtime:
            if self.tickspeed < self.ticklowspeed:
                j = self.sounds.mTicks(self.tickspeed)
                if j > 0:
                    self.tickspeed += 0.03
            else:
                self.sounds.mTicks(self.tickspeed)

        elif not self.slowtime:
            if self.tickspeed > self.tickhighspeed:
                k = self.sounds.mTicks(self.tickspeed)
                if k > 0:
                    self.tickspeed -= self.tickspeedrate
                    if self.tickspeedrate > 0.1:
                        self.tickspeedrate -= 0.01
                    else:
                        self.tickspeedrate = 0.1

        if self.playerhit:
            self.sounds.mHit()
            self.playerhit = False

        if self.fighterhit:
            self.sounds.mHit()
            self.fighterhit = False

    def run(self):
        self.sounds.playTheme()
        while self.menu_system.state != "quitgame":
            self.event_handler()
            self.update()
            self.draw()
            self.clock.tick(30)

if __name__ == '__main__':
    g = Game()
    g.run()
