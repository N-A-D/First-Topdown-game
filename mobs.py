'''
@author: Ned Austin Datiles
'''

import pygame as pg
from random import choice, uniform
from core_functions import collide_with_obstacles
from itertools import chain
from settings import *


class Mob(pg.sprite.Sprite):
    """
    This class represents an enemy object and its
    various attributes and abilities in game
    """

    def __init__(self, game, x, y):
        """
        Initializes a mob object for use in the game
        :param game: The game to which this mob will be employed
        :param x: x location in the plane
        :param y: y location in the plane
        """
        # Used to determine when the mob will be drawn
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        self.game = game
        pg.sprite.Sprite.__init__(self, self.groups)
        # Image copies are necessary because if were not
        # for the copy, any damages pasted onto the enemy
        # image would be replicated onto the other enemies
        # even if they haven't been damaged
        self.original_image = choice(game.enemy_imgs).copy()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = vec(x, y) * TILESIZE

        # Secondary rectangle for collisions is necessary
        # because rotation of the main rectangle warps its
        # size and causes issues with collision detection.
        self.hit_rect = ENEMY_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center

        # Positional, speed, and acceleration vectors
        self.pos = vec(self.rect.center)
        self.vel = vec(1, 0)
        self.acc = vec(0, 0)
        self.rot = 0

        self.speed = choice(ENEMY_SPEEDS)
        self.health = choice(ENEMY_HEALTH)
        self.is_damaged = False
        self.damage = choice(ENEMY_DAMAGE)

        # How fast this mob is able to track
        # the player
        self.seek_force = choice(SEEK_FORCE)
        self.desired = vec(0, 0)
        self.target = game.player
        # How often this mob will change targets while wondering
        self.last_target_time = 0

    def avoid_mobs(self):
        """
        Each mob will try to move away from each other
        so as to eliminate the issue where mob sprites
        would bunch up into one location
        :return: None
        """
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def hit(self):
        """
        Indicate that this mob has been hit
        :return: None
        """
        self.is_damaged = True

    def seek(self, target):
        """
        Gives a mob the ability to seek its target
        :param target: 
        :return: None
        """
        self.desired = (target - self.pos)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * self.speed
        else:
            self.desired *= self.speed
        steer = (self.desired - self.vel)
        if steer.length() > self.seek_force:
            steer.scale_to_length(self.seek_force)
        return steer

    def wander(self):
        """
        Gives a mob the ability to wander its environment
        :return: None
        """
        circle_pos = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = circle_pos + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        return self.seek(target)


    def update(self):
        """
        Update his mob's internal state
        :return: None
        """
        if self.health <= 0:
            self.kill()
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS ** 2:
            seek_force = self.seek(self.target.pos)
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.vel += seek_force
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_obstacles(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_obstacles(self, self.game.walls, 'y')
            self.rect.center = self.hit_rect.center
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.original_image, self.rot - 90)
            self.rect.center = self.pos

    def draw_health(self):
        """
        Each mob will have their health bars superimposed
        onto their sprite images so as to give the player
        visual indication that they've damaged this sprite
        :return: None
        """
        if self.health > 60:
            color = GREEN
        elif self.health > 30:
            color = YELLOW
        else:
            color = RED
        width = int(self.hit_rect.width * self.health / ENEMY_HEALTH[0])

        self.health_bar = pg.Rect(self.hit_rect.width // 3, 0, width, 7)

        if self.health < ENEMY_HEALTH[0]:
            pg.draw.rect(self.image, color, self.health_bar)
