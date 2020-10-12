import sys
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

        self.input_rect = pg.Rect(0, 0, 140, 32)
        self.colour_active = pg.Color('lightskyblue3')
        self.colour_passive = pg.Color('gray15')
        self.colour = self.colour_passive

        self.active = False
        self.interact = False
        self.object = None
        self.current_dialogue_num = ''

        # initialize all variables and do all the setup for a new game
        self.text = Text(self)
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.grasses = pg.sprite.Group()
        self.houses = pg.sprite.Group()
        self.blocks = pg.sprite.Group()
        self.trees = pg.sprite.Group()
        self.npcs = []


        self.onscreen_text = [] #((x, y), 'line')

        pg.mixer.music.load('Music/EpicGnomeQuestAmbience.mp3')
        pg.mixer.music.set_volume(0.65)
        pg.mixer.music.play(-1)

    def load_data(self):
        pass

    def new(self):
        for x in range(0, 30):
            for y in range(0, 30):
                Grass(self, x, y)
        #Around Well
        for x in range(2, 5):
            Wall(self, x, 5)
            Wall(self, x, 9)
        for y in range(6, 9):
            Wall(self, 1, y)
        for y in range(6, 7):
            Wall(self, 5, y)
        for y in range(8, 9):
            Wall(self, 5, y)
        # wall down
        for y in range(0, 2):
            Wall(self, 9, y)
        for y in range(3, 15):
            Wall(self, 9, y)
        self.draw_house(12, 3, 3)
        self.draw_house(16, 3, 3)
        self.draw_house(20, 3, 3)
        self.draw_trees()

        timmy = NPC(self, 3, 7, '004', 'Timmy')
        Well(self, 3, 7)
        jeff = NPC(self, 12, 10, '001', 'Jeff')
        self.npcs = [timmy, jeff]
        self.npcs[1].npc_movement_grid()
        self.player = Player(self, 21, 5)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.draw()
            if not self.check_interact():
                self.npcs[1].random_movement()
            self.draw_on_screen_text()
            self.check_active()
            self.update()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        pg.display.flip()

    def draw_house(self, x, y, size):
        Block(self, x+1, y-1)
        for x in range(x, (x + size)):
            Block(self, x, y)
        House(self, x-2, y-1)

    def draw_trees(self):
        self.draw_tree(3, 3)
        self.draw_tree(7, 4)
        self.draw_tree(11, 4)
        self.draw_tree(13, 1)
        for x in range(10, 22):
            if x % 2:
                self.draw_tree(x, 12)

    def draw_tree(self, x, y):
        Block(self, x, y)
        Tree(self, x, y)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)

    def talk(self):
        self.current_dialogue_num = self.text.talk(self.object.name, self.current_dialogue_num, self.input)
        self.draw_input_text()
        self.input = ''
        if self.current_dialogue_num == '0':
            i = 0
            for npc in self.npcs:
                if npc.name == self.object.name:
                    self.npcs[i].dialogue_num = '003'
                i += 1
            self.current_dialogue_num = ''
            self.interact = False

    def draw_text(self, dialogue, x=0, y=0):
        text_surface = self.base_font.render(dialogue, True, (WHITE))
        x = ((self.object.x - 1) * 32)
        y = (((self.object.y - 4) * 32) + y)
        self.screen.blit(text_surface, (x, y))

    def draw_on_screen_text(self):
        for c, dialogue in self.onscreen_text:
            self.draw_text(dialogue, c[0], c[1])

    def draw_input_text(self):
        x = ((self.object.x - 1) * 32)
        y = ((self.object.y - 1) * 32)
        self.input_rect = pg.Rect(x, y, 140, 32)
        pg.draw.rect(self.screen, self.colour, self.input_rect, 2)
        text_surface = self.base_font.render(self.user_text, True, (WHITE))
        self.screen.blit(text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

    def check_active(self):
        if self.active:
            self.colour = self.colour_active
        else:
            self.colour = self.colour_passive

    def check_interact(self):
        if self.interact or self.input is ['0', '1']:
            self.talk()
            return True
        else:
            return False

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

            if self.interact:
                # if event.type == pg.MOUSEBUTTONDOWN:
                #     if self.input_rect.collidepoint(event.pos):
                #         self.active = True
                #     else:
                #         self.active = False
                self.active = True
                if self.active is True:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            self.user_text = self.user_text[:-1]
                        elif event.key == pg.K_RETURN:
                            if self.user_text in ['0','1']:
                                self.input = self.user_text
                                self.user_text = ''
                                self.active = False
                                self.onscreen_text = []
                            else:
                                self.user_text = 'Invalid'
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
                self.onscreen_text = []

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
