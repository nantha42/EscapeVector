import pygame as py
import config
import font
import database


class Menu:
    def __init__(self):
        self.background = py.Surface((config.screen_width,config.screen_height))
        self.background.fill((0x8c, 0xbe, 0xd6))
        self.pause = False
        self.quit = False
        self.play = False
        self.showmenu = False
        self.backgroundImage = py.image.load("../images/background.png")
        self.backgroundImage = py.transform.scale(self.backgroundImage,(config.screen_width,config.screen_height))
        self.finalstates = ["start","levelmenu","quitgame","unpause","quitlevel","loadlevel","pause"]
        self.states = [ "mainmenu","gamemenu","levelmenu"]
        self.options = {"mainmenu":{"continue":"loadlast",
                                    "select level":"levelmenu",
                                    "option": "difficultymenu",
                                    "quit":"quitgame"},
                        "gamemenu":{"resume":"unpause","quit level":"quitlevel"},
                        "difficultymenu":{"easy":"none","normal":"none"},
                        "levelmenu":{"Levels":"loadlevel"},
                        }
        self.fontsystem = font.BigFontSystem()
        self.smfontsystem = font.SmallFontSystem()
        self.option_selected = "mainmenu"
        self.state = "mainmenu"
        self.current_option_texts = []
        self.menu_surface = py.Surface((250,300))
        self.optionon = -1
        self.database = database.Database()

    def draw(self,win):

        if self.option_selected == "mainmenu":
            win.blit(self.backgroundImage, (0, 0))
            i = 50 + 20

            self.menu_surface = py.Surface((250, 300))
            self.menu_surface = py.Surface.convert_alpha(self.menu_surface)
            self.menu_surface.fill((20, 20, 10, 200))
            self.current_option_texts = []
            ind = -1
            t,tr = self.fontsystem.draw("EscapeVector",(200,50,50))
            tr.x = 20
            tr.y = 20
            self.menu_surface.blit(t,tr)
            for option in self.options["mainmenu"]:
                ind+=1
                if self.optionon == ind:
                    t,tr = self.fontsystem.draw(option,(240,235,100))
                else:
                    t,tr = self.fontsystem.draw(option)
                tr.x = 20
                tr.y = i
                i+=45
                self.current_option_texts.append([option,t,tr])
                self.menu_surface.blit(t,tr)

            win.blit(self.menu_surface, (100, 200))

        elif  self.option_selected == "gamemenu":
            i = 50 + 20
            self.menu_surface = py.Surface((250, 300))
            self.menu_surface = py.Surface.convert_alpha(self.menu_surface)
            self.menu_surface.fill((20, 20, 10, 100))
            self.current_option_texts = []
            ind = -1
            t, tr = self.fontsystem.draw("EscapeVector", (200, 50, 50))
            tr.x = 20
            tr.y = 20
            self.menu_surface.blit(t, tr)
            for option in self.options["gamemenu"]:
                ind += 1
                if self.optionon == ind:
                    t, tr = self.fontsystem.draw(option, (240, 235, 100))
                else:
                    t, tr = self.fontsystem.draw(option)
                tr.x = 20
                tr.y = i
                i += 45
                self.current_option_texts.append([option, t, tr])
                self.menu_surface.blit(t, tr)

            win.blit(self.menu_surface, (100, 200))

        elif self.option_selected  == "levelmenu":
            win.blit(self.backgroundImage, (0, 0))
            i = 50 + 20
            self.menu_surface = py.Surface((780,250))
            self.menu_surface = self.menu_surface.convert_alpha()
            self.menu_surface.fill((20, 20, 10, 100))
            self.current_option_texts = []
            lock_image = py.image.load("../images/lock.png")
            lock_image = py.transform.scale(lock_image,(16,16))
            posx = 30
            for i in range(1,6):
                small_surface = py.Surface.convert_alpha(py.Surface((120, 120)))
                if self.optionon == i-1:
                    small_surface.fill((240,235,100,100))
                else:
                    small_surface.fill((20,20,10,100))
                text = "Level "+str(i)
                t,tr = self.fontsystem.draw(text)
                tr.centerx = 60
                tr.centery = 60
                small_surface.blit(t,tr)
                small_surface_rect = small_surface.get_rect()
                small_surface_rect.x = posx
                small_surface_rect.y = 65
                if i>self.database.levelunlocked:
                    small_surface.blit(lock_image,(60,100))

                self.current_option_texts.append([text,small_surface,small_surface_rect])
                self.menu_surface.blit(small_surface,small_surface_rect)
                posx += 150

            # tmp = self.menu_surface.get_rect()
            # print(tmp.x,tmp.y)
            self.optionon = -1

            back_surface = py.Surface.convert_alpha(py.Surface((50,30)))
            back_surface.fill((20,20,10,100))
            if self.optionon == 7:
                b,btr = self.smfontsystem.draw("back",(240,235,100))
            else:
                b,btr = self.smfontsystem.draw("back")
            btr.centerx = 25
            btr.centery = 15
            back_surface.blit(b,btr)
            bsr = back_surface.get_rect()
            bsr.centerx = 780/2
            bsr.y = 210
            self.current_option_texts.append(["back",back_surface,bsr])
            self.menu_surface.blit(back_surface,bsr)
            win.blit(self.menu_surface, (250, 200))




    def navigate(self,i):
        o = self.current_option_texts[i][0]

        if self.option_selected == "mainmenu":
            if o == "continue":
                self.state = "start"
            if o == "select level":
                self.option_selected = "levelmenu"
            if o == "quit":
                self.state = "quitgame"

        if self.option_selected == "gamemenu":
            if o == "resume":
                self.state = "start"

            if o == "quit level":
                self.option_selected = "mainmenu"
                self.state = "mainmenu"

        if self.option_selected == "levelmenu":
            if o == "Level 1":
                self.state = "start"
            if o == "Level 2":
                pass
            if o == "Level 3":
                pass
            if o == "Level 4":
                pass
            if o == "Level 5":
                pass

            if o == "back":
                self.option_selected = "mainmenu"

        if self.option_selected == "difficultymenu":
            if o == "easy":
                self.gamemode = "easy"
            if o == "normal":
                self.gamemode = "normal"

    def update(self,mousepos,clicked,escape):
        if escape:
            if self.state == "start":
                self.option_selected = "gamemenu"
                self.state = "mainmenu"
        i = -1
        m = list(mousepos)
        if self.option_selected == "mainmenu" or self.option_selected=="gamemenu":
            m[0] -= 100
            m[1] -= 200

        elif self.option_selected == "levelmenu":
            m[0]-=250
            m[1]-=200

        for op in self.current_option_texts:
            i+=1
            recta = op[2]

            if recta.collidepoint(m):
                self.optionon = i
                if clicked:
                    self.navigate(self.optionon)
                break
