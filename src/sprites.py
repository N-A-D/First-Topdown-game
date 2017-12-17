import pygame as pg
from random import uniform, choice, randint
from settings import TILESIZE, BULLET_LAYER, WEAPONS, EFFECTS_LAYER, \
    FLASH_DURATION, ITEMS_LAYER, BOB_RANGE, BOB_SPEED, PLAYER_MELEE_RECTS, vec, YELLOW
from core_functions import collide_hit_rect
import pytweening as tween
from math import sqrt


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
        """
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.rect = pg.Rect(x, y, width, height)
        self.hit_rect = self.rect.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(self.rect.center)
        self.radius = sqrt(self.hit_rect.width ** 2 + self.hit_rect.height ** 2)

    def update(self):
        self.rect = self.game.camera.apply(self)
        self.hit_rect = self.rect.copy()
        self.pos = vec(self.rect.center)


class BulletPassableWall(Obstacle):
    """
    Obstacles that are short enough for the player to shoot over
    """
    def __init__(self, game, x, y, width=TILESIZE, height=TILESIZE):
        super().__init__(game, x, y, width, height)
        self.game.bullet_passable_walls.add(self)


class Wall(Obstacle):
    """
    Obstacles the obstruct view and movement
    """
    def __init__(self, game, x, y, width=TILESIZE, height=TILESIZE):
        super().__init__(game, x, y, width, height)
        self.game.walls.add(self)


class _Wall(Obstacle):
    """
    Obstacles used by the mobs for collision avoidance
    """
    def __init__(self, game, x, y, width=TILESIZE, height=TILESIZE):
        super().__init__(game, x, y, width, height)
        self.game._walls.add(self)


class LevelEnd(Obstacle):
    """
    An obstacle which signals the end of the level when the player collides with it.
    The level ends iff the player has met the requirements for the end of the level.
    """
    def __init__(self, game, x, y, width, height):
        super().__init__(game, x, y, width, height)
        self.game.walls.add(self)
        self.passable = False

    def update(self):
        if len(self.game.mobs) == 0:
            self.passable = True


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
        self.hit_rect = pg.Rect(self.rect.x, self.rect.y, 45, 45)
        self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.75, 1)
        self.spawn_time = pg.time.get_ticks()
        # Damage and penetration depreciation are inversely proportional
        # As the damage decreases, the chance for this bullet to stop upon
        # hitting another enemy increases by the same rate
        self.damage = damage
        self.penetration_depreciation = WEAPONS['penetration depreciation'][self.weapon]

    def _update_pos(self):
        self.pos += self.vel * self.game.dt
        self.hit_rect.center = self.pos
        self.rect.center = self.hit_rect.center

    def _wall_collisions(self):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()

    def _mob_collisions(self):
        mobs = pg.sprite.spritecollide(self, self.game.mobs, False, collided=collide_hit_rect)
        if mobs:
            if uniform(0, 1) <= self.penetration_depreciation:
                self.kill()
            self.damage *= .75
            self.penetration_depreciation *= 1.25

            for mob in mobs:
                mob.health -= self.damage
                mob.pos += vec(WEAPONS[self.game.player.weapon]['damage'] // 10, 0).rotate(-self.game.player.rot)

    def update(self):
        """
        Update this bullet's internal state
        :return: None
        """
        self._update_pos()
        self._wall_collisions()
        self._mob_collisions()

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
    def __init__(self, game, x, y, _type, index=None):
        """
        Initiliazes this Item object
        :param game: the game 
        :param pos: where on the level this item is located
        :param img: the item image
        """
        self._type = _type  # Used to index into item info dictionary
        self.item_index = index
        self.layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.pickup_items[_type]
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.x = x
        self.rect.y = y
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


class SwingArea(pg.sprite.Sprite):
    """
    This class represents the area that the player swings their weapon.
    Any enemy caught in this area is dealt damage.
    """

    def __init__(self, game, pos, direction, weapon):
        """
        Damage area effect constuctor
        :param game: The game object
        :param pos: the position to place this damage area
        :param direction: in what direction the player is facing
        """
        self.groups = game.swingAreas
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        self.rect = PLAYER_MELEE_RECTS[weapon]
        self.hit_rect = self.rect.copy()
        self.direction = direction
        if self.direction == 'E':
            self.rect.midleft = pos
        elif self.direction == 'NE':
            self.rect.bottomleft = pos
        elif self.direction == 'N':
            self.rect.midbottom = pos
        elif self.direction == 'NW':
            self.rect.bottomright = pos
        elif self.direction == 'W':
            self.rect.midright = pos
        elif self.direction == 'SW':
            self.rect.topright = pos
        elif self.direction == 'S':
            self.rect.midtop = pos
        elif self.direction == 'SE':
            self.rect.topleft = pos
        self.hit_rect.center = self.rect.center
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        """
        Updates the state of this swing area
        :return:
        """
        if pg.time.get_ticks() - self.spawn_time > WEAPONS['animation times'][self.game.player.weapon]['melee']:
            self.kill()
        if self.direction == 'E':
            self.rect.midleft = self.game.player.hit_rect.midright
        elif self.direction == 'NE':
            self.rect.bottomleft = self.game.player.hit_rect.topright
        elif self.direction == 'N':
            self.rect.midbottom = self.game.player.hit_rect.midtop
        elif self.direction == 'NW':
            self.rect.bottomright = self.game.player.hit_rect.topleft
        elif self.direction == 'W':
            self.rect.midright = self.game.player.hit_rect.midleft
        elif self.direction == 'SW':
            self.rect.topright = self.game.player.hit_rect.bottomleft
        elif self.direction == 'S':
            self.rect.midtop = self.game.player.hit_rect.midbottom
        elif self.direction == 'SE':
            self.rect.topleft = self.game.player.hit_rect.bottomright