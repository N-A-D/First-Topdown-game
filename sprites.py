'''
@author: Ned Austin Datiles
'''
import pygame as pg
from random import uniform, choice, randint
from settings import *
from core_functions import collide_hit_rect
import pytweening as tween

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
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.rect.x = x * width
        self.rect.y = y * height
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.radius = self.rect.width * 0.7071
        self.pos = self.rect.center


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
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.8, 1.2)
        self.spawn_time = pg.time.get_ticks()
        # Damage and penetration depreciation are inversely proportional
        # As the damage decreases, the chance for this bullet to stop upon
        # hitting another enemy increases by the same rate
        self.damage = damage
        self.penetration_depreciation = .25

    def update(self):
        """
        Update this bullet's internal state
        :return: None
        """
        self.pos += self.vel * self.game.dt
        self.hit_rect.center = self.pos
        self.rect.center = self.hit_rect.center
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.sprite.spritecollide(self, self.game.mobs, False, collided=collide_hit_rect):
            if uniform(0, 1) <= self.penetration_depreciation:
                self.kill()
            self.damage *= .75
            self.penetration_depreciation *= 1.25
        # If the bullet has travelled a certain distance this removes it
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.weapon]['bullet_lifetime'] or self.damage <= 0:
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
        """
        Update this sprite's internal state
        :return: None
        """
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, img):
        """
        Initiliazes this Item object
        :param game: the game 
        :param pos: where on the level this item is located
        :param img: the item image
        """
        self.layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = img
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        """
        Bobbing motion for an item
        :return:
        """
        # How much to move from the starting position
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class WeaponPickup(Item):
    def __init__(self, game, pos):
        types = ['rifle', 'shotgun', 'handgun']
        self.type = choice(types)
        img = game.pickup_items[self.type]
        super().__init__(game, pos, img)
        self.ammo_boost = 1
        if self.type == 'rifle' or self.type == 'shotgun':
            self.ammo_boost = randint(2, 4)
        elif self.type == 'handgun':
            self.ammo_boost = randint(2, 6)

    def update(self):
        super().update()

class MiscPickup(Item):
    AMMO_BOOST = 5
    HEALTH_BOOST = 25
    def __init__(self, game, pos):
        types = ['ammo', 'health']
        self.type = choice(types)
        img = game.pickup_items[self.type]
        super().__init__(game, pos, img)

    def update(self):
        super().update()