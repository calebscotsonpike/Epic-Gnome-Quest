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
        self.base_font = pg.font.Font(None, 32)
        self.user_text = ''
        self.input = ''

        self.input_rect = pg.Rect(200, 200, 140, 32)
        self.colour_active = pg.Color('lightskyblue3')
        self.colour_passive = pg.Color('gray15')
        self.colour = self.colour_passive

        self.active = False
        self.interact = False
        self.object = None

        # initialize all variables and do all the setup for a new game
        self.text = Text(self)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, 10, 10)
        self.npcs = []

    def load_data(self):
        pass

    def new(self):
        john = NPC(self, 3, 3, '003', 'John')
        jeff = NPC(self, 20, 10, '001', 'Jeff')
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
            self.check_interact()
            self.check_active()
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

    def talk(self):
        off = self.text.talk(self.object.name, self.object.dialogue_num, self.input)
        self.draw_input_text()
        if off is True:
            self.interact = False

    def draw_text(self, dialogue, line):
        text_surface = self.base_font.render(dialogue, True, (WHITE))
        self.screen.blit(text_surface, (0, line))

    def draw_input_text(self):
        pg.draw.rect(self.screen, self.colour, self.input_rect, 2)
        text_surface = self.base_font.render(self.user_text, True, (WHITE))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

    def check_active(self):
        if self.active:
            self.colour = self.colour_active
        else:
            self.colour = self.colour_passive

    def check_interact(self):
        if self.interact or self.input is [0, 1]:
            self.talk()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False

            if self.active is True:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        self.user_text = self.user_text[:-1]
                    elif event.key == pg.K_RETURN:
                        self.input = self.user_text
                        self.user_text = ''
                        self.active = False
                    else:
                        self.user_text += event.unicode

            elif event.type == pg.KEYDOWN:
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

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
