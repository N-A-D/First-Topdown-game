'''
@author: Ned Austin Datiles
'''
import pygame as pg
from random import uniform, choice, randint
from settings import *

vec = pg.math.Vector2


class Obstacle(pg.sprite.Sprite):
    """
    This class represents obstacles in the game
    """

    def __init__(self, game, x, y, width, height):
        """
        Obstacle initialization
        :param game: The game object to which this obstacle belongs
        :param x: The x location of this obstacle
        :param y: The y location of this obstacle
        :param width: The width of this obstacle
        :param height: The height of this obstacle
        """
        # When this obstacle will be drawn to the screen
        self._layer = WALL_LAYER
        self.groups = game.walls, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((width, height))
        self.image.fill(SANDYBROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x * width
        self.rect.y = y * height
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)


class Bullet(pg.sprite.Sprite):
    """
    This class represents bullets in the game
    """

    def __init__(self, game, pos, dir, damage):
        """
        Bullet initialization
        :param game: The game object to which this bullet belongs
        :param pos: Where this bullet originated in the form of a vector
        :param dir: In which direction this bullet will travel
        :param damage: How much damage this bullet carries in flight
        """
        # When this bullet will be drawn to the screen
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Indicate from which firearm was this bullet shot from
        # Used to retrieve attributes about the bullet
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
        """
        Update this bullet's internal state
        :return: 
        """
        self.pos += self.vel * self.game.dt
        self.hit_rect.center = self.pos
        self.rect.center = self.hit_rect.center
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        # If the bullet has travelled a certain distance this removes it
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.weapon]['bullet_lifetime']:
            self.kill()


class MuzzleFlash(pg.sprite.Sprite):
    """
    This class represents muzzle flashes that come from
    Shooting guns in the game
    """

    def __init__(self, game, pos):
        """
        Muzzle flash initialization
        :param game: The game object to which this muzzle flash belongs to
        :param pos: The location where this muzzle flash will appear represented as a vector
        """
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(WEAPONS[game.player.weapon]['muzzle flash range'][0],
                       WEAPONS[game.player.weapon]['muzzle flash range'][1])
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = self.pos
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, 15, 15)
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class MeleeHitBox(pg.sprite.Sprite):
    """
    This class represents the damage area when the player swings their 
    weapon in an attempt to push back mobs in the game. 
    This is achieved my placing a rectangle in the same compass direction
    that the player is facing. When mobs collide with this rectangle, they
    will get pushed back. 
    """

    def __init__(self, game, pos, direction, action):
        """
        MeleeHitBox initialization
        :param game: The game object to which this melee box belongs to
        :param pos: The location where this melee box will appear
        :param direction: The compass direction used for the physical placement of the rectangle
        :param action: the melee action that invoked this object
        """
        self.groups = game.melee_box
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = PLAYER_MELEE_RECT
        self.pos = pos
        self.action = action
        if direction == 'E':
            self.rect.midleft = pos
        elif direction == 'NE':
            self.rect.bottomleft = pos
        elif direction == 'N':
            self.rect.midbottom = pos
        elif direction == 'NW':
            self.rect.bottomright = pos
        elif direction == 'W':
            self.rect.midright = pos
        elif direction == 'SW':
            self.rect.topright = pos
        elif direction == 'S':
            self.rect.midtop = pos
        elif direction == 'SE':
            self.rect.topleft = pos

        self.spawn_time = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        # Removes this hit box when the player concludes their melee animation
        if now - self.spawn_time > WEAPON_ANIMATION_TIMES[self.game.player.weapon][self.action] // 4:
            self.kill()


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, *type):
        self.layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.pickup_items[type[0]]
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.variety = type[0]
        self.item_type = type[1]
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
