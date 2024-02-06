import pygame as pg
import math
vector = pg.math.Vector2


class Program:
    def __init__(self):
    #initialize game window, etc
        pg.init()
        # pg.mixer.init()
        #dimension of window
        self.winWidth = 500
        self.winLength = 281
        #window set-up
        self.screen = pg.display.set_mode(size=(self.winWidth, self.winLength))
        pg.display.set_caption("Shinobi Warrior")
        self.clock = pg.time.Clock()
        self.last_update = 0
        self.playing = False
        self.running = True
        self.bg_no = 1
        self.score = 0
        # self.font2 = pg.font.Font('fonts/Bank_Gothic_Medium_BT.ttf', 15)
        # self.font = pg.font.Font('fonts/Bank_Gothic_Medium_BT.ttf', 20)
    
    def show_start_screen(self):
    
        # self.high_score()
        self.opn = pg.image.load('pygame/images/background.png').convert_alpha()
        self.screen.blit(self.opn,(0,0)) 
        # self.screen.blit(self.font.render('Press Tab For Controls', True, (0, 0, 0), (255, 255, 255)), (100,150))
        # self.screen.blit(self.font.render('Press Space To Play', True, (0, 0, 0), (255, 255, 255)), (120,200))  
        # self.screen.blit(self.font2.render('High Score: {}'.format(self.h_score), True, (0, 0, 0), (255, 255, 255)), (350,0))        
        pg.display.flip()    
        # self.enter_key()
    
g = Program()
g.show_start_screen()
    
pg.quit()