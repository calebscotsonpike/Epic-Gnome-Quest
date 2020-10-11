import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.gnome_left = pg.image.load('Sprites/gnome_left.png').convert_alpha()
        self.gnome_right = pg.image.load('Sprites/gnome_right.png').convert_alpha()
        self.image = self.gnome_left
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        if dx > 0:
            self.image = self.gnome_right
        else:
            self.image = self.gnome_left
        if not (self.collide_with_wall(dx, dy) or self.collide_with_npc(dx, dy)):
            self.x += dx
            self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def collide_with_wall(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def collide_with_npc(self, dx=0, dy=0):
        for npc in self.game.npcs:
            if npc.x == self.x + dx and npc.y == self.y + dy:
                return True
        return False

    def interact(self, dx=1, dy=1):
        for npc in self.game.npcs:
            if npc.x == self.x + dx or npc.y == self.y + dy or npc.x == self.x - dx or npc.y == self.y - dy:
                self.game.interact = True
                self.game.object = npc
                self.game.current_dialogue_num = npc.dialogue_num


class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, dialogue_num, name):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        if name == 'Timmy':
            image = pg.image.load('Sprites/Timmy.png').convert_alpha()
        else:
            image = pg.image.load('Sprites/Jeff.png').convert_alpha()
        self.image = image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dialogue_num = dialogue_num
        self.name = name

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        wall = pg.image.load('Sprites/wall.png').convert_alpha()
        self.image = wall
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Well(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        well = pg.image.load('Sprites/well.png').convert_alpha()
        self.image = well
        #self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Grass(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.grasses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        grass = pg.image.load('Sprites/grass.png').convert_alpha()
        self.image = grass
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
