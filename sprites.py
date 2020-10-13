import pygame as pg
from settings import *
import random

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
        if not (self.collide_with_wall(dx, dy) or self.collide_with_npc(dx, dy) or self.collide_with_block(dx, dy)):
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

    def collide_with_block(self, dx=0, dy=0):
        for block in self.game.blocks:
            if block.x == self.x + dx and block.y == self.y + dy:
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
            self.image_left = pg.image.load('Sprites/Timmy.png').convert_alpha()
        else:
            self.image_left = pg.image.load('Sprites/Jeff_left.png').convert_alpha()
            self.image_right = pg.image.load('Sprites/Jeff_right.png').convert_alpha()
        self.image = self.image_left
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dialogue_num = dialogue_num
        self.name = name
        self.moved = False
        self.movement_array = []
        random.seed(1)

    def set_dialogue_num(self, new_dialogue_num):
        self.dialogue_num = new_dialogue_num

    def move(self, dx=0, dy=0):
        if dx > 0:
            self.image = self.image_right
        else:
            self.image = self.image_left
        if not self.collide_with_walls(dx, dy) and not self.collide_with_player(dx, dy):
            self.x += dx
            self.y += dy
            self.moved = True

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def npc_movement_grid(self):
        for x in range(2):
            for y in range(2):
                self.movement_array.append((x, y))

    def random_movement(self):
        value = random.randint(0, 1000)
        if value > 998:
            if self.moved:
                self.move(-1, 0)
                self.moved = False
            else:
                self.move(1, 0)
                self.moved = True

    def collide_with_player(self, dx=0, dy=0):
        if self.game.player.x == self.x + dx and self.game.player.y == self.y + dy:
            return True
        return False

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False


class Block(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.blocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        block = pg.image.load('Sprites/grass.png').convert_alpha()
        self.image = block
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class House(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.houses
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        house = pg.image.load('Sprites/house.png').convert_alpha()
        self.image = house
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Object(pg.sprite.Sprite):
    def __init__(self, game, sprite_path, x, y, collide=0):
        if collide == 1:
            self.groups = game.all_sprites, game.objects, game.walls
        else:
            self.groups = game.all_sprites, game.objects
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        image = pg.image.load(sprite_path).convert_alpha()
        self.image = image
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
