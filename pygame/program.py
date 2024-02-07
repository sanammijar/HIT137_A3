import pygame as pg

class Program:
    def __init__(self):
        # initialize game window, etc
        pg.init()
        self.winWidth = 1280
        self.winLength = 800
        self.screen = pg.display.set_mode(size=(self.winWidth, self.winLength))
        pg.display.set_caption("Nepja - A Fighter")
        self.clock = pg.time.Clock()
        self.last_update = 0
        self.playing = False
        self.running = True
        self.bg_no = 1
        self.score = 0
    
    def show_start_screen(self):
        self.opn = pg.image.load('pygame/images/background.png').convert_alpha()
        self.screen.blit(self.opn, (0,0))
        text_surface = pg.font.SysFont(None, 40).render('Nepja - A Fightergit ', True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.winWidth // 2, self.winLength // 15))
        self.screen.blit(text_surface,text_rect)
        pg.display.flip()
        
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
    
    def run(self):
        while self.running:
            self.show_start_screen()
        
        pg.quit()

g = Program()
g.run()