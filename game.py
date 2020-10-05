import pygame as pg
import sys
from settings import *
from sprites import *
from text import Text

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        pg.font.init()
        self.user_text = ''

    def load_data(self):
        pass

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.text = Text(self)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, 10, 10)
        john = NPC(self, 3, 3, '001', 'john')
        jeff = NPC(self, 20, 10, '001', 'jeff')
        self.npcs = [john, jeff]

        for x in range(1, 5):
            Wall(self, x, 1)
            Wall(self, x, 5)
        for y in range(1, 5):
            Wall(self, 1, y)
        for y in range(1, 3):
            Wall(self, 5, y)
        for y in range(4, 6):
            Wall(self, 5, y)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.draw()
            self.update()


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        pg.display.flip()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)

    def talk(self, npc):
        self.text.talk(npc)

    def draw_text(self, dialogue):
        base_font = pg.font.Font(None, 32)
        text_surface = base_font.render(dialogue, True, (WHITE))
        self.screen.blit(text_surface, (10, 10))


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player.move(dx=1)
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.move(dy=1)
                if event.key == pg.K_SPACE:
                    self.player.interact()
                    #if event.key == pg.KEYDOWN:
                        #self.user_text = event.unicode


    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass