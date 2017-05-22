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
        self.current_rot = 0

        self.speed = choice(ENEMY_SPEEDS)
        self.health = choice(ENEMY_HEALTH)
        self.is_damaged = False
        self.damage = choice(ENEMY_DAMAGE)
        self.wander_time = choice(WANDER_TIMES)

        # How fast this mob is able to track
        # the player
        self.seek_force = choice(SEEK_FORCE) * self.speed
        self.desired = vec(0, 0)
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
        self.desired = target - self.pos
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * self.speed
        else:
            self.desired *= self.speed
        steer = self.desired - self.vel
        if steer.length() > self.seek_force:
            steer.scale_to_length(self.seek_force)
        return steer

    def wander(self):
        """
        Gives a mob the ability to wander its environment
        :return: None
        """
        if self.vel.length() != 0:
            circle_pos = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
            target = circle_pos + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
            return self.seek(target)

    def avoid_obstacles(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if hits:
            for obstacle in hits:
                approaching_wall = False
                if self.pos.x > obstacle.hit_rect.right - 25:
                    approaching_wall = True
                    self.desired = vec(-self.speed, self.vel.y)

                if self.pos.x < obstacle.hit_rect.left + 25:
                    approaching_wall = True
                    self.desired = vec(self.speed, self.vel.y)

                if self.pos.y > obstacle.hit_rect.bottom - 25:
                    approaching_wall = True
                    self.desired = vec(self.speed, self.vel.y)

                if self.pos.y > obstacle.hit_rect.top + 25:
                    approaching_wall = True
                    self.desired = vec(self.speed, self.vel.y)

                if approaching_wall:
                    steer = self.desired - self.vel
                    if steer.length() > self.seek_force:
                        steer.scale_to_length(self.seek_force)
                    self.acc = steer

    def update(self):
        """
        Update his mob's internal state
        :return: None
        """
        if self.health <= 0:
            self.kill()
        # target_dist = pg.mouse.get_pos() - self.pos #self.game.player.pos - self.pos
        # if target_dist.length_squared() < DETECT_RADIUS ** 2:
        self.acc = self.wander()
        self.vel += self.acc * self.game.dt
        if self.vel.length() > self.speed:
            self.vel.scale_to_length(self.speed)
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        self.hit_rect.centerx = self.pos.x

        if collide_with_obstacles(self, self.game.walls, 'x'):
            self.avoid_obstacles()

        self.hit_rect.centery = self.pos.y

        if collide_with_obstacles(self, self.game.walls, 'y'):
            self.avoid_obstacles()

        self.rot = self.vel.angle_to(vec(1, 0))
        self.image = pg.transform.rotozoom(self.original_image, self.rot - 90, 1).copy()
        self.rect.center = self.hit_rect.center

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
