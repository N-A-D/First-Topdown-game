'''
@author: Ned Austin Datiles
'''
import pygame as pg
from random import uniform, choice, randint
from settings import GREEN, WEAPONS, FLASH_DURATION, BULLET_LAYER, EFFECTS_LAYER, WALL_LAYER

vec = pg.math.Vector2


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = WALL_LAYER
        self.groups = game.walls, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((width, height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * width
        self.rect.y = y * height
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)


class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.weapon = game.player.weapon
        self.image = pg.transform.rotozoom(game.bullet_images[WEAPONS[game.player.weapon]['bullet_size']],
                                           game.player.rot, 1)
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, 15, 15)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1)
        self.spawn_time = pg.time.get_ticks()
        self.damage = damage

    def update(self):
        self.pos += self.vel * self.game.dt
        self.hit_rect.center = self.pos
        self.rect.center = self.hit_rect.center
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.weapon]['bullet_lifetime']:
            self.kill()


class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, 15, 15)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()
