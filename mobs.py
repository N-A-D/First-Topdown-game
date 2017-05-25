'''
@author: Ned Austin Datiles
'''

import pygame as pg
from random import choice, uniform, randint
from core_functions import collide_with_obstacles, collide_hit_rect
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
        self.vel = vec(randint(-1, 1), randint(-1, 1))
        self.acc = vec(0, 0)
        self.rot = 0
        self.current_rot = 0

        self.speed = choice(ENEMY_SPEEDS)
        self.health = choice(ENEMY_HEALTH)
        self.damage = choice(ENEMY_DAMAGE)
        self.wander_time = choice(WANDER_TIMES)

        # How fast this mob is able to track
        # the player
        self.seek_force = choice(SEEK_FORCE) * self.speed
        self.desired = vec(0, 0)
        # How often this mob will change targets while wondering
        self.last_target_time = 0

    def seek(self, target):
        """
        Gives a mob the ability to seek its target
        :param target: 
        :return: Vector2 representing the desired velocity
        """
        self.desired = target - self.pos
        dist = self.desired.length()
        self.desired.normalize_ip()
        self.desired *= self.speed
        # if dist < APPROACH_RADIUS:
        #     self.desired *= dist / APPROACH_RADIUS * self.speed
        # else:
        #     self.desired *= self.speed
        steer = self.desired - self.vel
        if steer.length() > self.seek_force:
            steer.scale_to_length(self.seek_force)
        return steer

    def wander(self):
        """
        Gives a mob the ability to wander its environment
        :return: Vector2 representing the desired velocity
        """

        circle_pos = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        target = circle_pos + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.acc += self.seek(target)

    def avoid_obstacles(self):
        """
        Gives a mob the ability to perceive obstacles in its vicinity
        and avoid them by moving in the opposite direction
        :return: None
        """
        hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
        if hits:
            sum = vec(0, 0)
            count = 0
            for obstacle in hits:
                if self.pos.x < obstacle.hit_rect.right + 15:
                    sum += vec(self.speed, self.vel.y)
                    count += 1
                if self.pos.x > obstacle.hit_rect.left - 15:
                    sum += vec(-self.speed, self.vel.y)
                    count += 1
                if self.pos.y < obstacle.hit_rect.bottom + 15:
                    sum +=  vec(self.vel.x, self.speed)
                    count += 1
                if self.pos.y > obstacle.hit_rect.top - 15:
                    sum += vec(self.vel.x, -self.speed)
                    count += 1

            sum /= count
            sum.normalize()
            sum *= self.speed
            steer = sum - self.vel

            if steer.length() > self.seek_force:
                steer.scale_to_length(self.seek_force)
            self.acc += steer

    def avoid_mobs(self):
        """
        Each mob will try to move away from each other
        so as to eliminate the issue where mob sprites
        would bunch up into one location
        :return: None
        """
        #mobs = pg.sprite.spritecollide(self, self.game.mobs, False, collide_hit_rect)
        #if mobs:
        sum = vec(0, 0)
        count = 0
        for mob in self.game.mobs:
            diff = self.pos - mob.pos
            dist = diff.length()
            if 0 < dist < AVOID_RADIUS:
                diff.normalize_ip()
                diff /= dist
                sum += diff
                count += 1

        if count > 0:
            sum /= count
            sum.normalize()
            sum *= self.speed
            steer = sum - self.vel
            if steer.length() > self.seek_force:
                steer.scale_to_length(self.seek_force)
            self.acc += steer

    def update(self):
        """
        Update his mob's internal state
        :return: None
        """
        if self.health <= 0:
            self.kill()
        self.wander()
        self.avoid_mobs()
        self.vel += self.acc * self.game.dt
        if self.vel.length() > self.speed:
            self.vel.scale_to_length(self.speed)
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.hit_rect.centerx = self.pos.x
        collide_with_obstacles(self, self.game.walls, 'x')
        #self.avoid_obstacles()
        self.hit_rect.centery = self.pos.y
        collide_with_obstacles(self, self.game.walls, 'y')
            #self.avoid_obstacles()
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
